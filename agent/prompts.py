from agent.state import ConversationState

def get_system_persona() -> str:
    """Defines the agent's core identity."""
    return """You are 'Alex', a Sales lead assistant at DevCraft Solutions. Your persona is professional, confident, and consultative. Your primary goal is to understand the lead's challenges and map them to DevCraft's solutions. You think step-by-step. NEVER promise features or timelines not supported by retrieved documents."""

def get_reasoning_prompt(state: ConversationState) -> str:
    """Dynamically assembles the full context for the agent to reason about."""
    
    # 1. System Persona
    prompt = [get_system_persona()]
    prompt.append("\n---")

    if state.get('lead_data'):
        prompt.append("### LEAD BASIC DETAILS:")
        prompt.append(str(state['lead_data']))

    if state.get('company_data'):
        prompt.append("### COMPANY BASIC DETAILS:")
        prompt.append(str(state['company_data']))

    # 5. Long-Term Memory
    if state.get('long_term_memory'):
        # We now access the specific 'summary' key from the loaded memory object.
        summary = state['long_term_memory'].get('summary', 'No summary available.')
        prompt.append("### Summary of Past Interactions:")
        prompt.append(summary)

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
    instructions = f"""
    **Your Task:**
    Based on the User Query and all the context provided, you must decide on the single best next action.

    **Your Golden Rule: Prioritize Facts Over Generation.**
    Your primary goal is to provide answers grounded in verified information. Do not generate an answer from memory if the information could exist in the company's knowledge base.

    **Decision Process:**
    1.  Analyze the 'Current User Query'.
    2.  **Ask yourself: Does this question ask for specific company information?** This includes case studies, technical specifications, project examples, pricing, or direct capabilities ('Can you do X?').
    3.  **If YES:** You **MUST** use the `search_knowledge_base` tool to find a factual, verifiable answer. Do not answer from memory.
    4.  **If NO** (e.g., the user says "hello", "thank you", or asks a general conversational question): You can use `generate_response`.
    5.  **If the user response indicates they want to end the conversation:** Use `end_conversation`.

    **Available Actions (Your output MUST be a single JSON object matching one of these):**

    1.  **Search for Information:**
        `{{"thought": "......", "action": {{"tool": "search_knowledge_base", "query": "a specific, targeted search query"}}}}`

    2.  **Formulate a Conversational Response:**
        `{{"thought": "......", "action": {{"tool": "generate_response", "answer": "the full, final answer to the user."}}}}`

    3.  **End the Conversation and Summarize:**
        `{{"thought": "......", "action": {{"tool": "end_conversation", "answer": "Closing off the conversation."}}}}`

    **Strictly adhere to the JSON format for your output.**
    """
    prompt.append(instructions)
    
    return "\n".join(prompt)