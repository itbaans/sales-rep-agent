from typing import List, Dict, TypedDict, Optional

class ConversationState(TypedDict):
    """Defines the state of the conversation."""
    lead_id: str
    user_input: Optional[str]
    messages: List[Dict]
    
    # Data loaded at the beginning
    lead_data: Dict
    company_data: Dict
    
    # State updated at the end
    conversation_summary: Optional[str]
    lead_insights: Optional[Dict]
    next_actions: Optional[List[str]]