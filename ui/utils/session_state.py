import streamlit as st
from typing import Any, Optional

def initialize_session_state():
    """Initialize session state variables"""
    
    # Core application state
    if 'knowledge_initialized' not in st.session_state:
        st.session_state.knowledge_initialized = False
    
    # Conversation state
    if 'current_lead' not in st.session_state:
        st.session_state.current_lead = None
    
    if 'conversation_active' not in st.session_state:
        st.session_state.conversation_active = False
    
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    
    # Agent state
    if 'agent_graph' not in st.session_state:
        st.session_state.agent_graph = None
    
    if 'conversation_config' not in st.session_state:
        st.session_state.conversation_config = {}

def get_session_state(key: str, default: Any = None) -> Any:
    """Get a value from session state"""
    return getattr(st.session_state, key, default)

def set_session_state(key: str, value: Any):
    """Set a value in session state"""
    setattr(st.session_state, key, value)

def clear_session_state(key: str):
    """Clear a specific key from session state"""
    if hasattr(st.session_state, key):
        delattr(st.session_state, key)

def reset_conversation_state():
    """Reset conversation-related session state"""
    set_session_state('conversation_active', False)
    set_session_state('conversation_history', [])
    set_session_state('conversation_config', {})

def get_conversation_config(lead_id: str) -> dict:
    """Get or create conversation config for a lead"""
    configs = get_session_state('conversation_config', {})
    
    if lead_id not in configs:
        configs[lead_id] = {
            "configurable": {"thread_id": lead_id}
        }
        set_session_state('conversation_config', configs)
    
    return configs[lead_id]