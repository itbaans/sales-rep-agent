from agent.state import ConversationState
from agent.services.turn_manager import TurnManager

def get_system_persona() -> str:
    """Defines the agent's core identity."""
    return """You are 'Zain', a Sales lead assistant at Systems Ltd. Your persona is professional, confident, and consultative. Your primary goal is to understand the lead's challenges and map them to Systems Ltd's solutions. 

You are trained to:
- Detect buying signals (budget mentions, timeline urgency, decision authority)
- Identify objections early (price, timing, authority, need)
- Qualify leads progressively (budget fit, authority level, need urgency, engagement)
- Adapt your communication style based on conversation stage

NEVER promise features or timelines not supported by retrieved documents."""

def get_opening_prompt(state: ConversationState) -> str:
    # Retrieve data from state
    lead = state.get('lead_data', {})
    memory = state['long_term_memory'].get('detailed_memory', '') if state.get('long_term_memory') else None
    # If no memory exists, we set it to an empty string
    if not memory:
        memory = "No past interactions recorded."
    company = state.get('company_data', {})

    # Construct a clear instruction for the LLM
    base_instruction = (
        "Using the provided data, craft an opening statement. "
        "Decide if it's an initial outreach or follow-up, reference past interaction if any. "
        "Important: respond ONLY with the opening statement itself—do NOT include any lead-in text such as 'Okay, here's...' or additional commentary."
    )

    # Assemble context sections
    company_section = f"## COMPANY DATA ##\n{company!r}"
    lead_section = f"## LEAD DATA ##\n{lead!r}"
    memory_section = f"## PAST MEMORY ##\n{memory!r}" if memory else "## PAST MEMORY ##\nNone"

    # Build message list for Gemini LLM
    prompt = [
        f"##SYSTEM: {get_system_persona()}",
        f"{base_instruction}\n{company_section}\n{lead_section}\n{memory_section}"
    ]

    return "\n".join(prompt)

def get_reasoning_prompt(state: ConversationState) -> str:
    """Assemble a complete, structured reasoning prompt for the agent."""
    
    prompt = [get_system_persona(), "\n---"]

    # Lead & Company Info
    if state.get('lead_data'):
        prompt.append("### LEAD BASIC DETAILS:")
        prompt.append(str(state['lead_data']))
    if state.get('company_data'):
        prompt.append("### COMPANY BASIC DETAILS:")
        prompt.append(str(state['company_data']))
    
    # Conversation Context
    if state.get('conversation_stage'):
        prompt.append(f"### CURRENT CONVERSATION STAGE: {state['conversation_stage']}")
    if state.get('lead_qualification_score'):
        prompt.append(f"### LEAD QUALIFICATION SCORE: {state['lead_qualification_score']}")
    if state.get('detected_objections'):
        prompt.append(f"### PREVIOUSLY DETECTED OBJECTIONS: {state['detected_objections']}")
    if state.get('buying_signals_detected'):
        prompt.append(f"### BUYING SIGNALS DETECTED: {state['buying_signals_detected']}")

    # Long-Term Memory Summary
    if state.get('long_term_memory'):
        summary = state['long_term_memory'].get('summary', 'No summary available.')
        prompt.append("### SUMMARY OF PAST INTERACTIONS:")
        prompt.append(summary)

    # Conversation History
    if state.get('messages'):
        prompt.append("\n### CONVERSATION HISTORY:")
        for msg in state['messages']:
            prompt.append(f"{msg['role'].capitalize()}: {msg['content']}")

    # Retrieved Docs
    if state.get('retrieved_docs'):
        prompt.append("\n### RETRIEVED KNOWLEDGE BASE INFO:")
        for doc in state['retrieved_docs']:
            prompt.append(f"- {doc}")

    # Actions for Current Turn
    if state.get('current_turn_actions'):
        prompt.append("\n### CURRENT TURN ACTIONS:")
        for action in state['current_turn_actions']:
            prompt.append(f"- {action}")

    # Previous Turn Scratchpad
    if state.get('scratchpad'):
        recent_summary = TurnManager.get_recent_turns_summary(state, num_turns=3)
        prompt.append("\n### PREVIOUS TURN ANALYSIS:")
        prompt.append(recent_summary)

    # Current Query
    prompt.append("\n---")
    prompt.append(f"### CURRENT USER QUERY:\n{state['user_input']}")

    # Refined Instructions
    prompt.append("\n---")
    instructions = """
**TASK FLOW**
1. Analyze the user query for buying signals, objections, and qualification data.
2. Update the conversation stage if needed.
3. Select ONE best next action based on stage, detected signals, and available info.

**SIGNAL DEFINITIONS**
- Buying signals: mentions of budget, timelines, demo requests, "next steps"
- Objections: concerns about price, timing, decision authority, or need
- Qualification: budget range, authority level, timeline, pain points

**STAGE GUIDELINES**
- DISCOVERY: Ask about pain points, solutions, decision process
- INTEREST: Share case studies, technical details
- OBJECTION_HANDLING: Address concerns using knowledge base
- CLOSING: Suggest demos, proposals, or next meetings

**SEARCH PRIORITY**
1. Company-specific tools (highest)
2. General knowledge base (lower)
3. Direct response (lowest)

**TOOL SELECTION RULES**
- Avoid repeating the same search tool in a single turn if it failed to return useful results.
- If all search tools have been tried without relevant results, generate a context-based response.

**TOOL DECISION MAP**
- Case studies / success stories → `search_company_case_studies`
- Technical capabilities / integrations → `search_technical_capabilities`
- Pricing / cost / budget → `search_pricing_models`
- Company profile / history → `search_company_profile`
- General questions (not covered above) → `search_knowledge_base`
- Detected new signals or stage change needed → `update_conversation_context`
- Direct reply possible without search → `generate_response`
- If user is indicating ending the conversation or the current conversation indicates about ending the conversation → `end_conversation`

**AVAILABLE ACTIONS (Pick ONE)**
1. `{"thought": "...", "action": {"tool": "search_company_case_studies", "keywords": "..."}}`
2. `{"thought": "...", "action": {"tool": "search_technical_capabilities", "keywords": "..."}}`
3. `{"thought": "...", "action": {"tool": "search_pricing_models", "keywords": "..."}}`
4. `{"thought": "...", "action": {"tool": "search_company_profile", "keywords": "..."}}`
5. `{"thought": "...", "action": {"tool": "search_knowledge_base", "query": "..."}}`
6. `{"thought": "...", "action": {"tool": "update_conversation_context", "stage": "...", "signals": [...], "qualification_updates": {...}}}`
7. `{"thought": "...", "action": {"tool": "generate_response", "answer": "..."}}`
8. `{"thought": "...", "action": {"tool": "end_conversation", "answer": "..."}}`

**STRICTLY** return JSON in the above format.
"""
    prompt.append(instructions)

    return "\n".join(prompt)
