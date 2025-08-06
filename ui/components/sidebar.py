import streamlit as st
import json
from pathlib import Path
from ui.utils.session_state import get_session_state, set_session_state
from agent.services.memory_manager import load_memory

def render_sidebar():
    """Render the sidebar with lead selection and conversation controls"""
    
    st.sidebar.markdown("### 👥 Lead Management")
    
    # Load available leads
    leads_file = Path("data/leads.json")
    if not leads_file.exists():
        st.sidebar.error("No leads file found!")
        return
    
    with open(leads_file, 'r') as f:
        leads = json.load(f)
    
    if not leads:
        st.sidebar.warning("No leads available")
        return
    
    # Lead selection
    current_lead = get_session_state('current_lead')
    lead_options = {f"{data['name']} ({data['company']})": lead_id 
                   for lead_id, data in leads.items()}
    
    selected_option = st.sidebar.selectbox(
        "Select Lead:",
        options=[""] + list(lead_options.keys()),
        index=0 if not current_lead else (
            list(lead_options.keys()).index(
                next(k for k, v in lead_options.items() if v == current_lead)
            ) + 1 if current_lead in lead_options.values() else 0
        )
    )
    
    if selected_option and selected_option != "":
        selected_lead_id = lead_options[selected_option]
        if selected_lead_id != current_lead:
            set_session_state('current_lead', selected_lead_id)
            # Clear conversation when switching leads
            set_session_state('conversation_history', [])
            set_session_state('conversation_active', False)
            st.rerun()
    
    # Conversation controls
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎛️ Controls")
    
    if current_lead:
        # Start/Reset conversation
        if not get_session_state('conversation_active'):
            if st.sidebar.button("🚀 Start Conversation", type="primary"):
                set_session_state('conversation_active', True)
                st.rerun()
        else:
            if st.sidebar.button("🔄 Reset Conversation"):
                set_session_state('conversation_history', [])
                set_session_state('conversation_active', False)
                st.rerun()
    
    # Lead memory summary
    if current_lead:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📝 Lead Memory")
        
        memory = load_memory(current_lead)
        if memory and memory.get('summary'):
            with st.sidebar.expander("Previous Interactions"):
                st.markdown(memory['summary'])
        else:
            st.sidebar.info("No previous interactions")
    
    # System status
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 System Status")
    
    knowledge_status = get_session_state('knowledge_initialized', False)
    st.sidebar.success("✅ Knowledge Base Ready" if knowledge_status else "❌ Knowledge Base Not Ready")
    
    if current_lead and get_session_state('conversation_active'):
        st.sidebar.success("✅ Conversation Active")
    else:
        st.sidebar.info("ℹ️ No Active Conversation")