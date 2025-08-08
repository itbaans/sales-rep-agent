import json
from agent.services.llm_service import get_llm
from agent.state import ConversationState
from agent.services.memory_manager import save_memory

def format_final_state_for_synthesis(state: ConversationState) -> str:
    """
    Helper to compile the entire final state into a comprehensive text block
    for the LLM to synthesize.
    """
    report = []
    report.append("### Final State Report for Synthesis ###")

    # Original Lead Data
    if state.get('lead_data'):
        report.append("\n--- Original Lead Profile ---")
        report.append(json.dumps(state['lead_data'], indent=2))

    # Initial Long-Term Memory (what we knew at the start)
    if state.get('long_term_memory'):
        report.append("\n--- Pre-existing Long-Term Memory ---")
        report.append(json.dumps(state['long_term_memory'], indent=2))
        
    # Full Conversation Transcript
    if state.get('messages'):
        report.append("\n--- Conversation Transcript ---")
        transcript = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in state['messages']])
        report.append(transcript)

    # Documents Retrieved During the Conversation
    if state.get('retrieved_docs'):
        report.append("\n--- Documents Retrieved During Conversation ---")
        report.append("\n".join([f"- {doc}" for doc in state['retrieved_docs']]))

    # Agent's Internal Thoughts (Scratchpad)
    if state.get('scratchpad'):
        report.append("\n--- Agent's Internal Reasoning (Scratchpad) ---")
        report.append("\n".join(state['scratchpad']))
        
    return "\n".join(report)


def create_enhanced_summary(detailed_memory: dict) -> str:
    """Create a more intelligent summary focusing on sales context"""
    if not detailed_memory:
        return "No summary available."

    llm = get_llm()
    memory_str = json.dumps(detailed_memory, indent=2)

    prompt = f"""
        Create a concise sales-focused summary from this structured lead memory. This summary will be used by the sales agent in future conversations.

        **Focus on:**
        - Current conversation stage and what was accomplished
        - Key pain points the lead confirmed
        - Their qualification level (budget, authority, urgency, engagement)
        - Any objections that need addressing
        - Next logical steps in the sales process

        **Memory Data:**
        ---
        {memory_str}
        ---

        **Write a natural paragraph summary that helps the sales agent pick up where they left off:**
        """

    summary = llm.invoke(prompt).content.strip()
    return summary

def update_summary_and_insights(state: ConversationState) -> ConversationState:
    print("---NODE: UPDATE_SUMMARY_AND_INSIGHTS (Enhanced with Conversation Intelligence)---")
    
    llm = get_llm()
    final_report = format_final_state_for_synthesis(state)
    
    # Enhanced detailed memory prompt with conversation intelligence
    detailed_prompt = f"""
        Analyze the following comprehensive 'Final State Report' and synthesize ALL information into a structured JSON object that represents the new state of knowledge about this lead.

        **Enhanced Analysis - Pay special attention to:**
        - Conversation stage progression (opening → discovery → interest → objection_handling → closing)
        - Lead qualification signals (budget authority, timeline urgency, need level)
        - Buying signals vs. objections detected
        - Communication style preferences (technical vs. business focused)
        - Specific pain points that resonated with the lead

        **Final State Report:**
        ---
        {final_report}
        ---

        **Output the enhanced JSON object:**
        {{
        "projects_of_interest": ["list of strings"],
        "key_pain_points_confirmed": ["list of strings"],
        "solutions_of_interest": ["list of strings"],
        "budget_confirmed": "string or null",
        "timeline_confirmed": "string or null",
        "decision_authority_level": "High/Medium/Low",
        "key_questions_asked_by_lead": ["list of strings"],
        "relevant_docs_provided": ["list of strings with context"],
        "buying_signals_detected": ["list of positive signals"],
        "objections_raised": ["list of concerns/objections"],
        "conversation_stage_reached": "discovery/interest/objection_handling/closing/nurturing",
        "lead_qualification_score": {{
            "budget_fit": 1-10,
            "authority_level": 1-10,
            "need_urgency": 1-10,
            "engagement_level": 1-10
        }},
        "communication_style_preference": "technical/business/mixed",
        "next_steps_agreed": ["list of strings"],
        "overall_sentiment": "Positive/Neutral/Negative/Mixed",
        "follow_up_timing": "immediate/1-3 days/1 week/1 month/longer",
        "miscellaneous_notes": "Any other relevant notes or observations"
        }}
        """
        
    try:
        response_str = llm.invoke(detailed_prompt).content
        cleaned_response_str = response_str.strip().replace('```json', '').replace('```', '')
        detailed_memory = json.loads(cleaned_response_str)
    except (json.JSONDecodeError, TypeError) as e:
        print(f"Warning: Failed to parse enhanced memory JSON. Error: {e}. Saving basic object.")
        detailed_memory = {
            "conversation_stage_reached": state.get('conversation_stage', 'discovery'),
            "lead_qualification_score": state.get('lead_qualification_score', {}),
            "buying_signals_detected": state.get('buying_signals_detected', []),
            "objections_raised": state.get('detected_objections', [])
        }

    if detailed_memory:
        print("---Generating enhanced in-context summary from detailed memory...---")
        in_context_summary = create_enhanced_summary(detailed_memory)
    else:
        in_context_summary = "No detailed memory was generated."

    save_memory(state['lead_id'], detailed_memory, in_context_summary)
    state['is_end'] = True  # Mark conversation as ended
    return state
