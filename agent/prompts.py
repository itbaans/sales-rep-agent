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
    if state.get('stage_guidance'):
        prompt.append(f"### CURRENT CONVERSATION GUIDANCE: {state['stage_guidance']}")
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
1. Use the provided stage guidance, detected signals, objections, and qualification updates (already generated).
2. Based on the current stage guidance and available context, select ONE best next action.
3. Generate the action in the required JSON format.

**SIGNAL DEFINITIONS (reference only)**
- Buying signals: mentions of budget, timelines, demo requests, "next steps"
- Objections: concerns about price, timing, decision authority, or need
- Qualification: budget range, authority level, timeline, pain points

**STAGE GUIDELINES (already updated separately by stage guidance)**
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
- Direct reply possible without search → `generate_response`
- If user is indicating ending the conversation or the current conversation indicates about ending the conversation → `end_conversation`

**AVAILABLE ACTIONS (Pick ONE)**
1. `{"thought": "...", "action": {"tool": "search_company_case_studies", "keywords": "..."}}`
2. `{"thought": "...", "action": {"tool": "search_technical_capabilities", "keywords": "..."}}`
3. `{"thought": "...", "action": {"tool": "search_pricing_models", "keywords": "..."}}`
4. `{"thought": "...", "action": {"tool": "search_company_profile", "keywords": "..."}}`
5. `{"thought": "...", "action": {"tool": "search_knowledge_base", "query": "..."}}`
6. `{"thought": "...", "action": {"tool": "generate_response", "answer": "..."}}`
7. `{"thought": "...", "action": {"tool": "end_conversation", "answer": "..."}}`

**STRICTLY** return JSON in the above format.
"""
    prompt.append(instructions)

    return "\n".join(prompt)

def get_stage_guidance_prompt(state: ConversationState) -> str:
    """
    Build a structured prompt for the LLM to generate stage guidance.
    The guidance should reflect emotional intelligence, 
    consider past guidance, and optionally update lead insights.
    """
    
    history_str = "\n".join(
        [f"User: {msg['user']}\nAgent: {msg['agent']}" for msg in state.messages]
    )

    past_guidance_str = state.stage_guidance or "None provided yet."
    
    lead_score_str = (
        f"Budget Fit: {state.lead_qualification_score.get('budget_fit', 'N/A')}, "
        f"Authority: {state.lead_qualification_score.get('authority', 'N/A')}, "
        f"Need Urgency: {state.lead_qualification_score.get('need_urgency', 'N/A')}, "
        f"Engagement: {state.lead_qualification_score.get('engagement', 'N/A')}"
        if state.lead_qualification_score else "Not yet evaluated."
    )
    
    objections_str = (
        ", ".join(state.detected_objections) if state.detected_objections else "None detected yet."
    )
    
    buying_signals_str = (
        ", ".join(state.buying_signals_detected) if state.buying_signals_detected else "None detected yet."
    )
    
    prompt = f"""
You are an expert sales coach with strong emotional intelligence.
Your task is to provide updated *Stage Guidance* for the sales agent
based on the ongoing conversation with a potential lead.

Conversation History:
{history_str}

Previous Stage Guidance:
{past_guidance_str}

Lead Insights so far:
- Qualification Score: {lead_score_str}
- Detected Objections: {objections_str}
- Buying Signals: {buying_signals_str}

Your tasks:
1. Write a short reflective passage (~3-5 sentences) that describes the **current stage of the conversation** with emotional intelligence. Include guidance on how the agent should move forward in a natural, empathetic way. 
   - If the previous guidance is still relevant, make only small adjustments.
   - If the conversation has shifted significantly, adapt the advice accordingly.

2. Update the **lead qualification score** (budget_fit, authority, need_urgency, engagement) on a 1–5 scale based on any new signals. 
   - Only change values if the new evidence is strong enough.

3. Identify any new **objections** the lead may have raised (add them if new).  

4. Identify any new **buying signals** the lead may have shown (add them if new).  

Return your output in **strict JSON** format with the following structure:

{{
  "stage_guidance": "<your reflective passage here>",
  "lead_qualification_score": {{
      "budget_fit": <int 1–5>,
      "authority": <int 1–5>,
      "need_urgency": <int 1–5>,
      "engagement": <int 1–5>
  }},
  "detected_objections": [<list of objections>],
  "buying_signals_detected": [<list of signals>]
}}
"""
    
    return prompt

    