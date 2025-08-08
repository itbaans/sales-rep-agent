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
        response_str = llm.invoke(prompt).content
        state['messages'].append({
            "role": "agent",
            "content": response_str
        })
        TurnManager.start_new_turn(state, user_query=None)
        return state

    if state['messages'][-1]['role'] == 'user' and state['current_turn_actions'] is None:
        user_query = state['messages'][-1]['content']
        TurnManager.start_new_turn(state, user_query=user_query)

    prompt = get_reasoning_prompt(state)
    response_str = llm.invoke(prompt).content
    
    TurnManager.add_action_to_current_turn(
        state,
        action_type="llm_reasoning",
        details={
            "reasoning_output": response_str,
            "prompt_length": len(prompt)
        }
    )
    
    #print(response_str)
    return state

def update_conversation_context(state: ConversationState, stage: str, signals: list, qualification_updates: dict) -> str:
    """Update conversation stage and qualification data"""
    # Update stage
    state['conversation_stage'] = stage
    
    # Initialize or update qualification score
    if not state.get('lead_qualification_score'):
        state['lead_qualification_score'] = {
            "budget_fit": 5,
            "authority_level": 5,
            "need_urgency": 5,
            "engagement_level": 5
        }
    
    # Update qualification scores
    for key, value in qualification_updates.items():
        if key in state['lead_qualification_score']:
            state['lead_qualification_score'][key] = max(1, min(10, value))
    
    # Track signals
    if not state.get('buying_signals_detected'):
        state['buying_signals_detected'] = []
    if not state.get('detected_objections'):
        state['detected_objections'] = []
        
    # Categorize signals
    for signal in signals:
        if any(word in signal.lower() for word in ["budget", "timeline", "demo", "next", "start"]):
            if signal not in state['buying_signals_detected']:
                state['buying_signals_detected'].append(signal)
        elif any(word in signal.lower() for word in ["expensive", "sure", "think", "time", "other"]):
            if signal not in state['detected_objections']:
                state['detected_objections'].append(signal)
    
    return f"Updated to {stage} stage. Qualification score: {state['lead_qualification_score']}. New signals: {signals}"

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
        print(f"Case Studies Result: {result}")
        
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
        print(f"Technical Capabilities Result: {result}")
        
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
        print(f"Pricing Models Result: {result}")
        
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
        print(f"Company Profile Result: {result}")
        
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
        print(f"Knowledge Base Result: {result}")
        
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
        
    elif tool == "update_conversation_context":
        stage = action.get("stage", "discovery")
        signals = action.get("signals", [])
        qualification_updates = action.get("qualification_updates", {})
        
        context_result = update_conversation_context(state, stage, signals, qualification_updates)
        
        TurnManager.add_action_to_current_turn(
            state,
            action_type="context_update",
            details={
                "tool": "update_conversation_context",
                "stage": stage,
                "signals": signals,
                "qualification_updates": qualification_updates,
                "result": context_result,
                "thought": thought
            }
        )
        
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