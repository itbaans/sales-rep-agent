import json
from agent.state import ConversationState
from agent.services.memory_manager import load_memory

def load_initial_data(state: ConversationState) -> ConversationState:
    print("---NODE: LOAD_INITIAL_DATA---")
    lead_id = state['lead_id']
    
    # Load LTM
    state['long_term_memory'] = load_memory(lead_id)
    
    # Load lead data
    with open('data/leads.json', 'r') as f:
        all_leads = json.load(f)
    state['lead_data'] = all_leads.get(lead_id, {})
    
    # Load company data
    with open('data/company_data.json', 'r') as f:
        state['company_data'] = json.load(f)
        
    # Initialize other state fields
    state['messages'] = []
    state['scratchpad'] = []
    state['retrieved_docs'] = []
    
    return state