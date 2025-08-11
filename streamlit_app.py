import streamlit as st
import json
from datetime import datetime
from typing import Dict, Any, List
import os
from pathlib import Path

# Import your existing modules
from vectorstores.create_knowledge_bases import initialize_vector_knowledge, initialize_json_knowledge
from agent.services.memory_manager import load_memory
from ui.components.sidebar import render_sidebar
from ui.utils.conversation_handler import ConversationHandler
from ui.components.chat import render_chat_interface
from ui.components.lead_info import render_lead_info
from ui.utils.session_state import initialize_session_state, get_session_state


# Page config
st.set_page_config(
    page_title="Systems Ltd - Sales Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f4e79, #2d5aa0);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .chat-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        min-height: 500px;
        max-height: 600px;
        overflow-y: auto;
    }
    
    .agent-message {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #1976d2;
    }
    
    .user-message {
        background-color: #f3e5f5;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #7b1fa2;
    }
    
    .sidebar-section {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 Systems Limited - Sales Agent</h1>
        <p>AI-Powered Sales Conversation Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize knowledge bases on first run
    if not st.session_state.get('knowledge_initialized', False):
        with st.spinner('Initializing knowledge bases...'):
            try:
                initialize_vector_knowledge()
                initialize_json_knowledge()
                st.session_state.knowledge_initialized = True
                st.success('Knowledge bases initialized successfully!')
            except Exception as e:
                st.error(f'Failed to initialize knowledge bases: {str(e)}')
                return
    
    # Create layout
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Sidebar content
        render_sidebar()
    
    with col2:
        # Main chat interface
        current_lead = get_session_state('current_lead')
        
        if current_lead:
            # Lead information panel
            render_lead_info(current_lead)
            
            # Chat interface
            render_chat_interface()
        else:
            st.info("👈 Please select a lead from the sidebar to start a conversation.")
            
            # Show available leads
            st.subheader("Available Leads")
            leads_file = Path("data/leads.json")
            if leads_file.exists():
                with open(leads_file, 'r') as f:
                    leads = json.load(f)
                
                for lead_id, lead_data in leads.items():
                    with st.expander(f"📋 {lead_data.get('name', 'Unknown')} - {lead_data.get('company', 'N/A')}"):
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.write(f"**Role:** {lead_data.get('role', 'N/A')}")
                        with col_b:
                            st.write(f"**Company:** {lead_data.get('company', 'N/A')}")
                        
                        if st.button(f"Start Conversation", key=f"start_{lead_id}"):
                            st.session_state.current_lead = lead_id
                            st.rerun()

if __name__ == "__main__":
    main()