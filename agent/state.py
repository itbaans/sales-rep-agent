from typing import List, Dict, TypedDict, Optional, Any

class ConversationState(TypedDict):
    """Defines the complete state of the agent's 'working memory'."""
    # Core identifiers
    lead_id: str
    user_input: Optional[str] # <-- Make explicitly Optional

    # Context Components
    long_term_memory: Dict[str, Any]
    messages: List[Dict]
    retrieved_docs: List[str]
    scratchpad: List[str]

    # Data loaded for the session
    lead_data: Dict
    company_data: Dict

    # Finalization outputs
    conversation_summary: Optional[str]
    next_actions: Optional[List[str]]