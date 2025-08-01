import json
from agent.state import ConversationState
from agent.prompts import get_reasoning_prompt
from agent.services.llm_service import get_llm
from agent.services.knowledge_retriever import search_knowledge_base

def think(state: ConversationState) -> ConversationState:
    print("---NODE: THINK---")
    prompt = get_reasoning_prompt(state)
    #print(prompt)
    llm = get_llm()
    
    response_str = llm.invoke(prompt).content
    state['scratchpad'].append(f"LLM Reasoning Output:\n{response_str}")
    print(response_str)

    # The LLM's JSON output is stored in the scratchpad for routing
    return state

def execute_tool(state: ConversationState) -> ConversationState:
    print("---NODE: EXECUTE_TOOL---")
    # Get the last reasoning step
    last_thought = state['scratchpad'][-1]
    
    try:
        action_json = json.loads(last_thought.split('```json\n')[-1].split('```')[0])
        action = action_json.get('action', {})
    except json.JSONDecodeError:
        # If LLM fails to produce valid JSON, fallback
        state['scratchpad'].append("Observation: Failed to parse action JSON from LLM. Will try to respond directly.")
        return state

    tool = action.get("tool")
    
    if tool == "search_knowledge_base":
        query = action.get("query", "")
        result = search_knowledge_base(query)
        print(result)
        observation = f"Observation: Found the following information: {result}"
        state['retrieved_docs'].append(result) # Add to dedicated doc storage
    else:
        observation = f"Observation: Unknown tool '{tool}'."

    state['scratchpad'].append(observation)
    return state