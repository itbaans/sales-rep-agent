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

# agent/services/memory_summarizer.py

import json
from agent.services.llm_service import get_llm

def create_in_context_summary(detailed_memory: dict) -> str:

    if not detailed_memory:
        return "No summary available."

    llm = get_llm()
    
    # The detailed memory is converted to a string to be included in the prompt
    memory_str = json.dumps(detailed_memory, indent=2)

    prompt = f"""
        Analyze the following structured JSON data which represents an agent's long-term memory about a sales lead. Your task is to convert this structured data into a concise, natural-language paragraph.

        This summary will be given back to the agent in its next conversation with this lead. Focus on the most important points that the agent should remember for future interactions.

        **Rules:**
        - Write in the third person (e.g., "The lead expressed...", "The agent provided...").
        - Focus on the most important takeaways: confirmed pain points, key interests, and the overall status of the conversation.

        **Structured Memory Data:**
        ---
        {memory_str}
        ---

        **Your summary**
        """

    summary = llm.invoke(prompt).content.strip()
    return summary

def update_summary_and_insights(state: ConversationState) -> ConversationState:
    
    print("---NODE: UPDATE_SUMMARY_AND_INSIGHTS (Full State Synthesis)---")
    
    llm = get_llm()
    # Create the comprehensive final report for the LLM
    final_report = format_final_state_for_synthesis(state)
    
    # --- Generate Detailed, Structured Memory (for the agent) ---
    detailed_prompt = f"""
        Analyze the following comprehensive 'Final State Report'. Your task is to synthesize ALL of this information into a single, structured JSON object that represents the new state of knowledge about this lead.

        **Rules:**
        - Your output must be a single JSON object.
        - Base your answers on the totality of the information: the original profile, the conversation, and any retrieved documents or agent thoughts.
        - If a fact is confirmed in the conversation (e.g., budget), use that as the source of truth over the original profile.
        - Sentiment should be your overall assessment (Positive, Neutral, Negative, Mixed).

        **Final State Report:**
        ---
        {final_report}
        ---

        **Output the final, synthesized JSON object and nothing else.**
        Use the following structure only and avoid any additional text:
        {{
        "key_pain_points_confirmed": ["list of strings"],
        "solutions_of_interest": ["list of strings"],
        "budget_confirmed": "string or null",
        "timeline_confirmed": "string or null",
        "key_questions_asked_by_lead": ["list of strings"],
        "relevant_docs_provided": ["list of strings from retrieved docs and why were they provided and what the interaction was regarding them"],
        "overall_sentiment": "Positive",
        "next_steps": ["list of strings"],
        "miscellaneous_notes": "Any other relevant notes or observations"
        }}
        """
    try:
        response_str = llm.invoke(detailed_prompt).content
        # A simple cleanup to handle potential markdown formatting
        cleaned_response_str = response_str.strip().replace('```json', '').replace('```', '')
        detailed_memory = json.loads(cleaned_response_str)
    except (json.JSONDecodeError, TypeError) as e:
        print(f"Warning: Failed to parse detailed memory JSON. Error: {e}. Saving empty object.")
        detailed_memory = {}

    if detailed_memory:
        print("---Generating in-context summary from detailed memory...---")
        in_context_summary = create_in_context_summary(detailed_memory)
    else:
        in_context_summary = "No detailed memory was generated."

    # Pass all three components to the save function
    save_memory(
        state['lead_id'], 
        detailed_memory,
        in_context_summary
    )
    
    return state