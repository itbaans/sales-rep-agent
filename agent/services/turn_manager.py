# agent/services/turn_manager.py
from datetime import datetime
from typing import Dict, List, Any
from agent.state import ConversationState

class TurnManager:
    """Manages turn-based scratchpad entries"""
    
    @staticmethod
    def start_new_turn(state: ConversationState, user_query: str) -> ConversationState:
        """Initialize a new turn with user query"""
        # Initialize turn counter if not exists
        if not state.get('turn_counter'):
            state['turn_counter'] = 0
        
        state['turn_counter'] += 1
        
        # Initialize current turn actions
        state['current_turn_actions'] = []
        
        # Add initial action - user query received
        if user_query is None:
            TurnManager.add_action_to_current_turn(
            state, 
            action_type="agent_opening",
            details={"agent_response": state['messages'][-1]['content']}
        )
        else:
            TurnManager.add_action_to_current_turn(
                state,
                action_type="user_query",
                details={"query": user_query}
            )

        return state
    
    @staticmethod
    def add_action_to_current_turn(state: ConversationState, action_type: str, details: Dict[str, Any]) -> ConversationState:
        """Add an action to the current turn's action list"""
        if not state.get('current_turn_actions'):
            state['current_turn_actions'] = []
            
        action_entry = {
            "timestamp": datetime.now().isoformat(),
            "action_type": action_type,
            "details": details
        }
        
        state['current_turn_actions'].append(action_entry)
        return state
    
    @staticmethod
    def finalize_turn(state: ConversationState, final_response: str) -> ConversationState:
        """Finalize the current turn and add it to scratchpad"""
        # Clear current turn actions
        if 'current_turn_actions' in state:
            state['current_turn_actions'].clear()  # Use .clear() method
        else:
            state['current_turn_actions'] = []
        
        return state
    