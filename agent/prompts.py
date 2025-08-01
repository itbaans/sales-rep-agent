from agent.state import ConversationState

def get_system_persona() -> str:
    """Defines the agent's core identity."""
    return """You are 'Alex', a Sales lead assistant at DevCraft Solutions. Your persona is professional, confident, and consultative. Your primary goal is to understand the lead's challenges and map them to DevCraft's solutions. You think step-by-step. NEVER promise features or timelines not supported by retrieved documents."""

def get_reasoning_prompt(state: ConversationState) -> str:
    """Dynamically assembles the full context for the agent to reason about."""
    
    # 1. System Persona
    prompt = [get_system_persona()]
    prompt.append("\n---")
    
    # 5. Long-Term Memory
    if state.get('long_term_memory'):
        prompt.append("### Long-Term Memory (Summary of Past Interactions):")
        prompt.append(str(state['long_term_memory']))

    # 2. Conversation History
    if state.get('messages'):
        prompt.append("\n### Current Conversation History:")
        for msg in state['messages']:
            prompt.append(f"{msg['role'].capitalize()}: {msg['content']}")

    # 3. Document Retrievals
    if state.get('retrieved_docs'):
        prompt.append("\n### Retrieved Information from Knowledge Base:")
        for doc in state['retrieved_docs']:
            prompt.append(f"- {doc}")

    # 4. Scratchpad (Previous thoughts)
    if state.get('scratchpad'):
        prompt.append("\n### Your Thought Process So Far:")
        prompt.append("\n".join(state['scratchpad']))

    # 6. User Query
    prompt.append("\n---")
    prompt.append(f"\n### Current User Query:\n{state['user_input']}")
    
    prompt.append("\n---")
    prompt.append("""
Based on ALL the information above, decide your next step. You have two choices:
1.  **Use a tool**: If you need more information to answer the user's query (e.g., search the knowledge base).
2.  **Respond to the user**: If you have enough information to provide a complete and helpful answer.

Your output MUST be a JSON object with two keys: "thought" and "action".
- "thought": A string explaining your reasoning for the chosen action.
- "action": A JSON object describing the action.
    - For a tool, it's: {"tool": "search_knowledge_base", "query": "what to search for"}
    - To respond, it's: {"tool": "generate_response", "answer": "The full, final answer to the user."}
    - To end, it's: {"tool": "end_conversation"}
""")
    
    return "\n".join(prompt)