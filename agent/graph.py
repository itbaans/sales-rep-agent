import json
from langgraph.graph import StateGraph, END, START
from agent.state import ConversationState
from agent.nodes import reasoning, finalization
from agent.services.turn_manager import TurnManager
from agent.nodes import stage_guidance

def should_invoke_stage_guidance(state: ConversationState) -> bool:
    turn_count = state.get("turn_counter", 0)
    N = 3  # frequency
    return turn_count % N == 0 and turn_count > 0

def should_continue_reasoning(state: ConversationState) -> str:
    # Get reasoning from current turn actions
    current_actions = state.get('current_turn_actions', [])

    if current_actions[-1]['action_type'] == 'agent_opening':
        final_answer = state['messages'][-1]['content']
        TurnManager.finalize_turn(state, final_answer)
        #print(final_answer)
        return "end_turn"

    reasoning_actions = [action for action in current_actions if action['action_type'] == 'llm_reasoning']
    
    if not reasoning_actions:
        return "execute_tool"  # No reasoning yet, continue
    
    last_reasoning = reasoning_actions[-1]['details']['reasoning_output']
    
    try:
        action_json = json.loads(last_reasoning.split('```json\n')[-1].split('```')[0])
        action = action_json.get('action', {})
    except json.JSONDecodeError:
        return "execute_tool"  # Continue if can't parse
    
    tool = action.get("tool")
    
    if tool == "generate_response":
        final_answer = action.get("answer", "I'm not sure how to respond to that.")
        
        # Finalize the turn before ending
        TurnManager.finalize_turn(state, final_answer)
        
        state['messages'].append({"role": "agent", "content": final_answer})
        #print(f"\nAgent: {state['messages'][-1]['content']}\n")
        #print(final_answer)
        return "end_turn"
        
    elif tool == "end_conversation":
        final_answer = action.get("answer", "Thank you for your time. Have a great day!")
        
        # Finalize the turn before ending conversation
        TurnManager.finalize_turn(state, final_answer)
        
        state['messages'].append({"role": "agent", "content": final_answer})
        #print(f"\nAgent: {state['messages'][-1]['content']}\n")
        #print(final_answer)
        return "end_conversation"
    else:
        return "execute_tool"


def create_agent_graph() -> StateGraph:
    workflow = StateGraph(ConversationState)

    # Add ALL nodes
    workflow.add_node("think", reasoning.think)
    workflow.add_node("execute_tool", reasoning.execute_tool)
    workflow.add_node("stage_guidance", stage_guidance.stage_guidance_node)  # NEW
    workflow.add_node("finalize", finalization.update_summary_and_insights)

    workflow.add_conditional_edges(
        START,
        should_invoke_stage_guidance,
        {
            True: "stage_guidance",
            False: "think"
        }
    )

    workflow.add_edge("stage_guidance", "think")

    # Main reasoning loop
    workflow.add_conditional_edges(
        "think",
        should_continue_reasoning,
        {
            "execute_tool": "execute_tool",
            "end_turn": END,
            "end_conversation": "finalize",
        },
    )

    # After tool execution → go back to guidance check
    workflow.add_edge("execute_tool", "think")

    workflow.add_edge("finalize", END)

    return workflow.compile()