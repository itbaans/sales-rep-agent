from agent.state import ConversationState
from agent.services.llm_service import get_llm
from langchain_core.messages import SystemMessage, HumanMessage

def generate_initial_prompt(state: ConversationState) -> ConversationState:
    print("---NODE: GENERATE_INITIAL_PROMPT---")
    lead = state['lead_data']
    company = state['company_data']['company_profile']
    
    prompt = f"""
    Hello {lead['name']}, this is Alex from {company['name']}.
    I saw that you're the {lead['role']} at {lead['company']} and are looking into a {lead['project_need']}. 
    Given your interest in {lead['tech_stack_preference']} and our expertise in that area, I believe we can help. 
    How are you currently handling your {lead['current_pain']}?
    """
    state['messages'].append({"role": "agent", "content": prompt})
    return state

def generate_response(state: ConversationState) -> ConversationState:
    print("---NODE: GENERATE_RESPONSE---")
    llm = get_llm()
    # You can build a more sophisticated prompt template here
    system_prompt = "You are a helpful sales assistant from DevCraft Solutions."
    
    messages_for_llm = [SystemMessage(content=system_prompt)]
    for msg in state['messages']:
        if msg['role'] == 'user':
            messages_for_llm.append(HumanMessage(content=msg['content']))

    response = llm.invoke(messages_for_llm)
    state['messages'].append({"role": "agent", "content": response.content})
    return state
