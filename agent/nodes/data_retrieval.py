import json
from agent.state import ConversationState

def retrieve_lead_data(state: ConversationState) -> ConversationState:
    print("---NODE: RETRIEVE_LEAD_DATA---")
    with open('data/leads.json', 'r') as f:
        all_leads = json.load(f)
    state['lead_data'] = all_leads.get(state['lead_id'], {})
    return state

def retrieve_company_data(state: ConversationState) -> ConversationState:
    print("---NODE: RETRIEVE_COMPANY_DATA---")
    with open('data/company_data.json', 'r') as f:
        state['company_data'] = json.load(f)
    return state