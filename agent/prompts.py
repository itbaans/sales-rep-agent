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

    # Enhanced: Add conversation stage context
    if state.get('conversation_stage'):
        prompt.append(f"### CURRENT CONVERSATION STAGE: {state['conversation_stage']}")
        
    if state.get('lead_qualification_score'):
        prompt.append(f"### LEAD QUALIFICATION SCORE: {state['lead_qualification_score']}")
        
    if state.get('detected_objections'):
        prompt.append(f"### PREVIOUSLY DETECTED OBJECTIONS: {state['detected_objections']}")
        
    if state.get('buying_signals_detected'):
        prompt.append(f"### BUYING SIGNALS DETECTED: {state['buying_signals_detected']}")

    # Long-Term Memory
    if state.get('long_term_memory'):
        summary = state['long_term_memory'].get('summary', 'No summary available.')
        prompt.append("### Summary of Past Interactions:")
        prompt.append(summary)

    # Conversation History
    if state.get('messages'):
        prompt.append("\n### Current Conversation History:")
        for msg in state['messages']:
            prompt.append(f"{msg['role'].capitalize()}: {msg['content']}")

    # Document Retrievals
    if state.get('retrieved_docs'):
        prompt.append("\n### Retrieved Information from Knowledge Base:")
        for doc in state['retrieved_docs']:
            prompt.append(f"- {doc}")

    if state.get('current_turn_actions'):
        prompt.append("\n### Current Turn Actions:")
        for action in state['current_turn_actions']:
            prompt.append(f"- {action}")

    # Enhanced: Structured Scratchpad (Previous Turn Summaries)
    if state.get('scratchpad'):
        prompt.append("\n### Your Previous Turn Analysis:")
        recent_summary = TurnManager.get_recent_turns_summary(state, num_turns=3)
        prompt.append(recent_summary)

    # User Query
    prompt.append("\n---")
    prompt.append(f"\n### Current User Query:\n{state['user_input']}")
    
    # Enhanced instructions with signal detection
    prompt.append("\n---")
    instructions = f"""
    **Your Task:**
    1. First, analyze the user query for buying signals and objections
    2. Update conversation stage if needed
    3. Choose the best next action based on the stage and signals

    **Signal Detection:**
    - Buying signals: budget mentions, timeline questions, demo requests, "next steps"
    - Objections: price concerns, timing issues, authority questions, need doubts
    - Qualification data: budget range, decision authority, project timeline, pain level

    **Stage-Specific Actions:**
    - DISCOVERY: Ask about pain points, current solutions, decision process
    - INTEREST: Provide relevant case studies, technical details
    - OBJECTION_HANDLING: Address concerns with facts from knowledge base
    - CLOSING: Suggest demos, proposals, next meetings

    **HIERARCHICAL SEARCH PRIORITY:**
    1. **Company-Specific Keyword Tools** (HIGHEST PRIORITY)
    2. **General Knowledge Base Search** (LOWER PRIORITY)
    3. **Response Generation** (LOWEST PRIORITY)

    **Search Decision Logic:**
    - If user asks about case studies, success stories, or "have you done X?" → Use `search_company_case_studies`
    - If user asks about technical capabilities, integrations, or "can you do X?" → Use `search_technical_capabilities`  
    - If user asks about pricing, cost, budget, or timelines → Use `search_pricing_models`
    - If user asks about company profile, history, or general info → Use `search_company_profile`
    - If user asks general questions not covered by above → Use `search_knowledge_base`

    ##DO NOT use the same search tool repeatedly in a single turn, if you could not find relevant information in the previous search##
    ##If you have exhausted all search options, generate a response based on current context##

    **Available Actions (Choose ONE):**

    1. **Company Case Studies Search:**
        `{{"thought": "User asking about [case studies/success stories/experience]. Using keyword search...", "action": {{"tool": "search_company_case_studies", "keywords": "relevant keywords only (e.g. 'healthcare CRM', 'fintech mobile')"}}}}`

    2. **Technical Capabilities Search:**
        `{{"thought": "User asking about [technical capabilities/integrations]. Using keyword search...", "action": {{"tool": "search_technical_capabilities", "keywords": "relevant keywords only (e.g. 'React integration', 'AWS deployment')"}}}}`

    3. **Pricing Information Search:**
        `{{"thought": "User asking about [pricing/cost/budget]. Using keyword search...", "action": {{"tool": "search_pricing_models", "keywords": "relevant keywords only (e.g. 'web app pricing', 'maintenance cost')"}}}}`

    4. **Company Profile Search:**
        `{{"thought": "User asking about [company profile/history]. Using keyword search...", "action": {{"tool": "search_company_profile", "keywords": "relevant keywords only (e.g. 'company history', 'founding story')"}}}}`

    5. **General Knowledge Base Search:**
        `{{"thought": "Question not covered by company-specific tools. Using general knowledge base...", "action": {{"tool": "search_knowledge_base", "query": "targeted search query"}}}}`

    6. **Update Conversation Context:**
        `{{"thought": "Detected [signals/objections]... Updating conversation stage...", "action": {{"tool": "update_conversation_context", "stage": "discovery/interest/objection_handling/closing", "signals": ["list of detected signals"], "qualification_updates": {{"budget_fit": 1-10, "authority_level": 1-10}}}}}}`

    7. **Generate Response:**
        `{{"thought": "Based on stage [X] and signals [Y]... No search needed...", "action": {{"tool": "generate_response", "answer": "stage-appropriate response"}}}}`

    8. **End Conversation:**
        `{{"thought": "User wants to end...", "action": {{"tool": "end_conversation", "answer": "Closing message"}}}}`

    **Strictly adhere to the JSON format for your output.**
    """
    prompt.append(instructions)
    
    return "\n".join(prompt)