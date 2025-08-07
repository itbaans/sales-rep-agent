import streamlit as st
from datetime import datetime
from typing import List, Dict, Any
from agent.graph import create_agent_graph
from ui.utils.session_state import get_session_state, set_session_state, get_conversation_config

class ConversationHandler:
    """Handles conversation logic between UI and agent graph"""
    
    def __init__(self):
        self.app = self._get_or_create_app()
    
    def _get_or_create_app(self):
        """Get or create the agent graph app"""
        if not get_session_state('agent_graph'):
            app = create_agent_graph()
            set_session_state('agent_graph', app)
            return app
        return get_session_state('agent_graph')
    
    def start_conversation(self, lead_id: str) -> str:
        """Start a new conversation with opening statement"""
        try:
            config = get_conversation_config(lead_id)
            initial_state = {"lead_id": lead_id}
            
            # Run the graph to get opening statement
            # The graph should handle the opening statement generation
            self.app.invoke(initial_state, config)
            
            # Extract the agent's opening message from the result
            messages = initial_state.get('messages', [])
            if messages:
                # Find the last agent message
                agent_messages = [msg for msg in messages if msg.get('role') == 'agent']
                if agent_messages:
                    return agent_messages[-1]['content']
            
            return "Hello! I'm Zain from Systems Limited. How can I help you today?"
            
        except Exception as e:
            st.error(f"Error starting conversation: {str(e)}")
            raise e
    
    def process_user_input(self, lead_id: str, user_input: str, conversation_history: List[Dict]) -> str:
        """Process user input and get agent response"""
        try:
            config = get_conversation_config(lead_id)
            
            # Prepare the state with conversation context
            current_state = {
                "lead_id": lead_id,
                "user_input": user_input,
                "messages": self._convert_history_to_messages(conversation_history)
            }
            
            # Process through the graph
            result = self.app.invoke(current_state, config)
            
            # Extract agent response
            messages = result.get('messages', [])
            if messages:
                # Get the last agent message
                agent_messages = [msg for msg in messages if msg.get('role') == 'agent']
                if agent_messages:
                    return agent_messages[-1]['content']
            
            return "I'm having trouble processing that. Could you please try again?"
            
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
        