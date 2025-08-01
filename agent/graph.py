import json
from langgraph.graph import StateGraph, END
from agent.state import ConversationState
from agent.nodes import data_retrieval, reasoning, finalization, interaction # <-- import interaction

def should_continue_reasoning(state: ConversationState) -> str:
    last_thought_str = state.get('scratchpad', [])[-1]
    action_json = json.loads(last_thought_str.split('```json\n')[-1].split('```')[0])
    action = action_json.get('action', {})
    if action.get("tool") == "generate_response":
        final_answer = action.get("answer", "I'm not sure how to respond to that.")
        state['messages'].append({"role": "agent", "content": final_answer})
        print(f"\nAgent: {state['messages'][-1]['content']}\n")
        return "end_turn"
    elif action.get("tool") == "end_conversation":
        final_answer = action.get("answer", "I'm not sure how to respond to that.")
        state['messages'].append({"role": "agent", "content": final_answer})
        print(f"\nAgent: {state['messages'][-1]['content']}\n")
        return "end_conversation"
    else:
        return "execute_tool"


def create_agent_graph() -> StateGraph:
    workflow = StateGraph(ConversationState)

    # Add ALL nodes, including the new one
    workflow.add_node("load_initial_data", data_retrieval.load_initial_data)
    workflow.add_node("generate_opening_statement", interaction.generate_opening_statement)
    workflow.add_node("think", reasoning.think)
    workflow.add_node("execute_tool", reasoning.execute_tool)
    workflow.add_node("finalize", finalization.update_summary_and_insights)
    workflow.add_node("process_user_input", interaction.process_user_input)

    # Set Entry Point
    workflow.set_entry_point("load_initial_data")

    # This new conditional edge is the key to solving the problem
    workflow.add_edge(
        "load_initial_data", "generate_opening_statement"
    )

    # The agent's opening statement ends its turn. It must wait for a user response.
    workflow.add_edge("generate_opening_statement", "process_user_input")

    # The main reasoning loop remains the same
    workflow.add_edge("process_user_input", "think")
    workflow.add_conditional_edges(
        "think",
        should_continue_reasoning,
        {
            "execute_tool": "execute_tool",
            "end_turn": "process_user_input",
            "end_conversation": "finalize",
        },
    )
    workflow.add_edge("execute_tool", "think")
    workflow.add_edge("finalize", END)

    return workflow.compile()