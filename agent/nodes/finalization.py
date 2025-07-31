from agent.state import ConversationState
from agent.services.memory_manager import save_memory

def update_summary_and_insights(state: ConversationState) -> ConversationState:
    print("---NODE: UPDATE_SUMMARY_AND_INSIGHTS---")
    # In a real app, an LLM would generate these from state['messages']
    state['conversation_summary'] = "Lead asked for a case study and was provided one. They seem interested in our HealthTech experience."
    lead_insights = {"key_interest_expressed": "HealthTech case study"}
    state['next_actions'] = ["Follow up with a detailed proposal.", "Schedule a demo."]

    # Save to Long-Term Memory
    save_memory(
        state['lead_id'], 
        state['conversation_summary'],
        lead_insights
    )
    return state