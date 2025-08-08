import streamlit as st
from datetime import datetime
from typing import List, Dict, Any
from agent.AgentAPI import get_agent_api
from ui.utils.session_state import get_session_state, set_session_state, get_conversation_config

class ConversationHandler:
    """Handles conversation logic between UI and agent graph"""
    
    def __init__(self):
        self.app = self._get_or_create_app()
    
    def _get_or_create_app(self):
        """Get or create the agent graph app"""
        if not get_session_state('agent_graph'):
            app = get_agent_api(get_session_state('current_lead'))
            set_session_state('agent_graph', app)
            return app
        return get_session_state('agent_graph')
    
    def start_conversation(self, lead_id: str) -> str:
        """Start a new conversation with opening statement"""
        try:
            # Run the graph to get opening statement
            # The graph should handle the opening statement generation
            return self.app.get_opening_statement(lead_id)
                    
        except Exception as e:
            st.error(f"Error starting conversation: {str(e)}")
            raise e
    
    def process_user_input(self, lead_id: str, user_input: str, conversation_history: List[Dict]) -> str:
        """Process user input and get agent response"""
        try:
            return self.app.process_message(lead_id, user_input)
            
        except Exception as e:
            st.error(f"Error processing user input: {str(e)}")
            raise e
    
    def _convert_history_to_messages(self, conversation_history: List[Dict]) -> List[Dict]:
        """Convert UI conversation history to agent message format"""
        messages = []
        
        for msg in conversation_history:
            messages.append({
                'role': msg['role'],
                'content': msg['content']
            })
        
        return messages
    
    def get_current_timestamp(self) -> str:
        """Get current timestamp for messages"""
        return datetime.now().strftime("%H:%M")
    
    def end_conversation(self, lead_id: str) -> bool:
        """End the current conversation and save state"""
        try:
            # Any cleanup logic here
            return True
        except Exception as e:
            st.error(f"Error ending conversation: {str(e)}")
            return False

# Simplified conversation handler for basic UI operations
class SimpleConversationHandler:
    """Simplified handler for basic conversation operations"""
    
    @staticmethod
    def get_mock_opening_statement(lead_name: str, company: str) -> str:
        """Generate a mock opening statement for testing"""
        return f"Hello! I'm Zain from Systems Limited. I understand you're {lead_name} from {company}. I'd love to discuss how our digital transformation solutions can help your organization. What challenges are you currently facing with your technology infrastructure?"
    
    @staticmethod
    def get_mock_response(user_input: str) -> str:
        """Generate a mock response for testing"""
        responses = {
            "hello": "Hello! Great to connect with you. What specific technology challenges is your organization facing?",
            "pricing": "I'd be happy to discuss our pricing models. We offer several options including fixed-price projects, time & materials, and value-based pricing. What type of project are you considering?",
            "capabilities": "Systems Limited specializes in digital transformation, data & AI solutions, cloud services, and business process outsourcing. We've successfully delivered projects for healthcare, banking, retail, and government sectors. Which area interests you most?",
            "default": "That's interesting. Could you tell me more about your specific requirements? I'd like to understand how Systems Limited can best support your goals."
        }
        
        user_lower = user_input.lower()
        
        for key, response in responses.items():
            if key in user_lower and key != "default":
                return response
        