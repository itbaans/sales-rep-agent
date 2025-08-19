from enum import Enum
from typing import List, Dict, TypedDict, Optional, Any

class ConversationStage(Enum):
    OPENING = "opening"
    DISCOVERY = "discovery"
    INTEREST = "interest"
    OBJECTION_HANDLING = "objection_handling"
    CLOSING = "closing"
    NURTURING = "nurturing"

class ConversationState(TypedDict):
    """Defines the complete state of the agent's 'working memory'."""
    # Core identifiers
    lead_id: str
    user_input: Optional[str]

    stage_guidance: Optional[str]

    #Conversation tracking
    lead_qualification_score: Optional[Dict[str, int]]  # budget_fit, authority, need_urgency, engagement
    detected_objections: Optional[List[str]]
    buying_signals_detected: Optional[List[str]]

    #turn tracking
    current_turn_actions: Optional[List[Dict[str, Any]]]  # Track actions in current turn
    turn_counter: Optional[int]  # Track which turn we're on

    # Context Components
    long_term_memory: Dict[str, Any]
    messages: List[Dict]
    retrieved_docs: List[str]

    # Data loaded for the session
    lead_data: Dict
    company_data: Dict

    is_end: bool