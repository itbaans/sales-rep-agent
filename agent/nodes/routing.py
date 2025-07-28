from agent.state import ConversationState

def router(state: ConversationState) -> str:
    print("---NODE: ROUTER---")
    last_user_message = state.get('user_input', '').lower()

    if "case study" in last_user_message or "tell me more about" in last_user_message:
        return "retrieve_from_knowledge_base"
    elif "bye" in last_user_message or "thank you" in last_user_message:
        return "end_conversation"
    else:
        return "generate_response"