from agent.state import ConversationState
from agent.services.knowledge_retriever import search_knowledge_base

def retrieve_from_knowledge_base(state: ConversationState) -> ConversationState:
    print("---NODE: RETRIEVE_FROM_KNOWLEDGE_BASE---")
    user_query = state.get('user_input', '')
    info = search_knowledge_base(user_query)
    
    # Add retrieved info to context for the next response generation
    info_message = f"Knowledge base information for you: {info}"
    state['messages'].append({"role": "agent", "content": info_message})
    return state