from agent.state import ConversationState

def update_conversation_summary(state: ConversationState) -> ConversationState:
    print("---NODE: UPDATE_CONVERSATION_SUMMARY---")
    # In a real app, you would use an LLM to summarize state['messages']
    state['conversation_summary'] = "The lead expressed interest in our React and AWS services and asked for a case study."
    return state

def update_lead_insights(state: ConversationState) -> ConversationState:
    print("---NODE: UPDATE_LEAD_INSIGHTS---")
    state['lead_insights'] = {"key_interest": "React, AWS", "next_step": "Send HealthTech case study"}
    return state

def update_next_actions(state: ConversationState) -> ConversationState:
    print("---NODE: UPDATE_NEXT_ACTIONS---")
    state['next_actions'] = ["Email Jennifer Martinez the HealthTech case study.", "Schedule follow-up for next week."]
    return state