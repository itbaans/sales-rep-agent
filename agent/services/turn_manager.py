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
        # Add final response to turn actions
        TurnManager.add_action_to_current_turn(
            state,
            action_type="final_response", 
            details={"response": final_response}
        )
        
        # Create comprehensive turn entry
        turn_entry = {
            "turn_number": state.get('turn_counter', 0),
            "user_query": state.get('user_input', ''),
            "actions_taken": state.get('current_turn_actions', []),
            "final_response": final_response,
            "turn_summary": TurnManager._generate_turn_summary(state),
            "timestamp": datetime.now().isoformat()
        }
        
        # Add to scratchpad
        if not state.get('scratchpad'):
            state['scratchpad'] = []
        state['scratchpad'].append(turn_entry)
        
        # Clear current turn actions
        state['current_turn_actions'] = []
        
        return state
    
    @staticmethod
    def _generate_turn_summary(state: ConversationState) -> str:
        """Generate a brief summary of what happened in this turn"""
        actions = state.get('current_turn_actions', [])
        if not actions:
            return "No actions taken"
            
        action_types = [action['action_type'] for action in actions]
        tools_used = [action['details'].get('tool', '') for action in actions if action['action_type'] == 'tool_execution']
        tools_used = [tool for tool in tools_used if tool]  # Remove empty strings
        
        summary_parts = []
        
        # Count different action types
        if 'llm_reasoning' in action_types:
            summary_parts.append("analyzed query")
        if tools_used:
            summary_parts.append(f"searched using: {', '.join(set(tools_used))}")
        if 'context_update' in action_types:
            summary_parts.append("updated conversation context")
        if 'final_response' in action_types:
            summary_parts.append("generated response")
            
        return " → ".join(summary_parts) if summary_parts else "completed turn"
    
    @staticmethod
    def get_recent_turns_summary(state: ConversationState, num_turns: int = 3) -> str:
        """Get a summary of recent turns for context"""
        scratchpad = state.get('scratchpad', [])
        if not scratchpad:
            return "No previous turns recorded."
            
        recent_turns = scratchpad[-num_turns:]
        summary_lines = []
        
        for turn in recent_turns:
            turn_num = turn.get('turn_number', 0)
            query = turn.get('user_query', '')[:50] + "..." if len(turn.get('user_query', '')) > 50 else turn.get('user_query', '')
            turn_summary = turn.get('turn_summary', '')
            summary_lines.append(f"Turn {turn_num}: '{query}' → {turn_summary}")
            
        return "\n".join(summary_lines)