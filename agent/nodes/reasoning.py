# agent/nodes/reasoning.py
import json
from agent.state import ConversationState
from agent.prompts import get_reasoning_prompt, get_opening_prompt
from agent.services.llm_service import get_llm
from agent.services.knowledge_retriever import search_knowledge_base, search_company_case_studies, search_technical_capabilities, search_pricing_models, search_company_profile
from agent.services.turn_manager import TurnManager

def think(state: ConversationState) -> ConversationState:
    print("---NODE: THINK---")

    llm = get_llm()

    if not state['messages']:
        prompt = get_opening_prompt(state)
        #print(prompt)
        response_str = llm.invoke(prompt).content
        state['messages'].append({
            "role": "agent",
            "content": response_str
        })
        TurnManager.start_new_turn(state, user_query=None)
        return state

    if state['messages'][-1]['role'] == 'user' and not state.get('current_turn_actions'):
        user_query = state['messages'][-1]['content']
        TurnManager.start_new_turn(state, user_query=user_query)

    prompt = get_reasoning_prompt(state)
    #print(prompt)
    response_str = llm.invoke(prompt).content
    
    TurnManager.add_action_to_current_turn(
        state,
        action_type="llm_reasoning",
        details={
            "reasoning_output": response_str,
        }
    )
    
    #print(response_str)
    return state


def execute_tool(state: ConversationState) -> ConversationState:
    print("---NODE: EXECUTE_TOOL---")
    
    # Get the last reasoning step from current turn actions
    current_actions = state.get('current_turn_actions', [])
    reasoning_actions = [action for action in current_actions if action['action_type'] == 'llm_reasoning']
    
    if not reasoning_actions:
        TurnManager.add_action_to_current_turn(
            state,
            action_type="error", 
            details={"error": "No reasoning output found to parse"}
        )
        return state
    
    last_reasoning = reasoning_actions[-1]['details']['reasoning_output']
    
    try:
        action_json = json.loads(last_reasoning.split('```json\n')[-1].split('```')[0])
        action = action_json.get('action', {})
        thought = action_json.get('thought', '')
    except json.JSONDecodeError:
        TurnManager.add_action_to_current_turn(
            state,
            action_type="error",
            details={"error": "Failed to parse action JSON from LLM reasoning"}
        )
        return state

    tool = action.get("tool")
    
    # HIERARCHICAL SEARCH IMPLEMENTATION WITH TURN TRACKING
    if tool == "search_company_case_studies":
        keywords = action.get("keywords", "")
        result = search_company_case_studies(keywords)
        #print(f"Case Studies Result: {result}")
        
        TurnManager.add_action_to_current_turn(
            state,
            action_type="tool_execution",
            details={
                "tool": "search_company_case_studies",
                "keywords": keywords,
                "result": result,
                "thought": thought
            }
        )
        state['retrieved_docs'].append(f"[CASE STUDIES] {result}")
        
    elif tool == "search_technical_capabilities":
        keywords = action.get("keywords", "")
        result = search_technical_capabilities(keywords)
        #print(f"Technical Capabilities Result: {result}")
        
        TurnManager.add_action_to_current_turn(
            state,
            action_type="tool_execution", 
            details={
                "tool": "search_technical_capabilities",
                "keywords": keywords,
                "result": result,
                "thought": thought
            }
        )
        state['retrieved_docs'].append(f"[TECHNICAL] {result}")
        
    elif tool == "search_pricing_models":
        keywords = action.get("keywords", "")
        result = search_pricing_models(keywords)
        #print(f"Pricing Models Result: {result}")
        
        TurnManager.add_action_to_current_turn(
            state,
            action_type="tool_execution",
            details={
                "tool": "search_pricing_models", 
                "keywords": keywords,
                "result": result,
                "thought": thought
            }
        )
        state['retrieved_docs'].append(f"[PRICING] {result}")

    elif tool == "search_company_profile":
        keywords = action.get("keywords", "")
        result = search_company_profile(keywords)
        #print(f"Company Profile Result: {result}")
        
        TurnManager.add_action_to_current_turn(
            state,
            action_type="tool_execution",
            details={
                "tool": "search_company_profile",
                "keywords": keywords,
                "result": result,
                "thought": thought
            }
        )
        state['retrieved_docs'].append(f"[COMPANY PROFILE] {result}")
    
    elif tool == "search_knowledge_base":
        query = action.get("query", "")
        result = search_knowledge_base(query)
        #print(f"Knowledge Base Result: {result}")
        
        TurnManager.add_action_to_current_turn(
            state,
            action_type="tool_execution",
            details={
                "tool": "search_knowledge_base",
                "query": query,
                "result": result, 
                "thought": thought
            }
        )
        state['retrieved_docs'].append(f"[GENERAL KB] {result}")

    else:
        TurnManager.add_action_to_current_turn(
            state,
            action_type="error",
            details={
                "error": f"Unknown tool '{tool}'",
                "thought": thought
            }
        )

    return state

