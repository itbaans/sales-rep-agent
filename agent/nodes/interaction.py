from agent.state import ConversationState
from agent.services.llm_service import get_llm


def generate_opening_statement(state: ConversationState) -> ConversationState:
    """
    Generates the initial, agent-initiated message based on lead data and memory.
    """
    print("---NODE: GENERATE_OPENING_STATEMENT---")
    lead = state['lead_data']
    ltm = state['long_term_memory']
    
    # Example of a slightly more dynamic opener
    last_summary = ltm.get('last_interaction_summary', '')
    
    if "Initial contact" in last_summary or not last_summary:
        prompt = f"""Hello {lead.get('name', 'there')}, this is Alex from DevCraft Solutions. I'm reaching out because I saw you're the {lead.get('role')} at {lead.get('company')} and noted your team's focus on projects involving {lead.get('tech_stack_preference', 'modern technologies')}. Given your work, I thought our expertise in legacy system modernization might be relevant. How are you currently approaching these challenges?"""
    else:
        # A follow-up prompt
        prompt = f"""Hi {lead.get('name', 'there')}, it's Alex from DevCraft Solutions again. Just following up on our last conversation where we discussed: '{last_summary}'. Do you have any further questions I can help with today?"""

    state['messages'].append({"role": "agent", "content": prompt})
    print(f"\nAgent: {state['messages'][-1]['content']}\n")
    return state


def process_user_input(state: ConversationState) -> ConversationState:

    user_input = input("Your response: ")
    state['user_input'] = user_input
    state['messages'].append({"role": "user", "content": user_input})
    return state


# def generate_response(state: ConversationState) -> ConversationState:
#     print("---NODE: GENERATE_RESPONSE---")
#     llm = get_llm()
#     # You can build a more sophisticated prompt template here
#     system_prompt = "You are a helpful sales assistant from DevCraft Solutions."
    
#     messages_for_llm = [SystemMessage(content=system_prompt)]
#     for msg in state['messages']:
#         if msg['role'] == 'user':
#             messages_for_llm.append(HumanMessage(content=msg['content']))

#     response = llm.invoke(messages_for_llm)
#     state['messages'].append({"role": "agent", "content": response.content})
#     return state
