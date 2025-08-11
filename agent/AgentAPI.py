"""
Simple API interface for the agent that can be used by both CLI and UI
"""
from agent.graph import create_agent_graph
from agent.services.memory_manager import load_memory
import json

from agent.services.memory_manager import load_memory
from agent.state import ConversationState

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
    with open('data/company_docs/system_in_context.txt', 'r') as f:
        state['company_data'] = f.read().strip()
        
    # Initialize turn tracking and other state fields
    state['messages'] = []
    state['scratchpad'] = []  # Now stores structured turn data
    state['retrieved_docs'] = []
    state['turn_counter'] = 0
    state['current_turn_actions'] = []

    state['is_end'] = False
    
    return state

class AgentAPI:
    def __init__(self, lead_id=None):
        self.app = create_agent_graph()
        if lead_id:
            self.state = load_initial_data({"lead_id": lead_id})
        else:
            self.state = None

    def initialize_knowledge(self):
        """Initialize knowledge bases"""
        try:
            from vectorstores.create_knowledge_bases import initialize_vector_knowledge, initialize_json_knowledge
            print("Initializing knowledge bases...")
            initialize_vector_knowledge()
            initialize_json_knowledge()
            print("Knowledge bases initialized!")
            return True
        except Exception as e:
            print(f"Error initializing knowledge bases: {e}")
            return False
    
    def get_opening_statement(self, lead_id: str) -> str:

        if self.state is None:
            self.state = load_initial_data({"lead_id": lead_id})

        """Get opening statement for a lead"""
        try:
            config = {"configurable": {"thread_id": f"{lead_id}"}}
            
            # Run graph to generate opening statement
            self.state = self.app.invoke(self.state, config)
            
            # Extract agent message
            messages = self.state.get('messages', [])
            agent_messages = [msg for msg in messages if msg.get('role') == 'agent']
            
            if agent_messages:
                return agent_messages[-1]['content']
            else:
                return "Hello! I'm Zain from Systems Limited. How can I help you today?"
                
        except Exception as e:
            print(f"Error getting opening statement: {e}")
            return "Hello! I'm Zain from Systems Limited. How can I help you today?"
    

    def set_user_response(self, user_input: str) -> str:
        if(self.state is None): print("IM NONE!")
        self.state['user_input'] = user_input
        self.state['messages'].append({"role": "user", "content": user_input})
        return


    def process_message(self, lead_id: str, user_input: str) -> str:
        """Process user message and get agent response"""
        try:
            config = {"configurable": {"thread_id": f"{lead_id}"}}
            
            # Prepare the state with conversation context
            self.state['user_input'] = user_input
            if self.state['messages'][-1]['role'] != 'user':
                self.state['messages'].append({"role": "user", "content": user_input})
            
            self.state = self.app.invoke(self.state, config)
            # Extract agent response
            result_messages = self.state.get('messages', [])
            agent_messages = [msg for msg in result_messages if msg.get('role') == 'agent']
            
            if agent_messages:
                # Get the last agent message (most recent response)
                return agent_messages[-1]['content']
            else:
                return "I'm having trouble processing that. Could you please try again?"
                
        except Exception as e:
            print(f"Error processing message: {e}")
            return "I'm having trouble processing that. Could you please try again?"
    
    def get_lead_info(self, lead_id: str) -> dict:
        """Get lead information and memory"""
        try:
            # Load lead data
            with open('data/leads.json', 'r') as f:
                leads = json.load(f)
            lead_data = leads.get(lead_id, {})
            
            # Load memory
            memory = load_memory(lead_id)
            
            return {
                'lead_data': lead_data,
                'memory': memory
            }
        except Exception as e:
            print(f"Error getting lead info: {e}")
            return {'lead_data': {}, 'memory': {}}

# Global instance
def get_agent_api(lead_id: str) -> AgentAPI:
    return AgentAPI(lead_id=lead_id)