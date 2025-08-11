from agent.AgentAPI import get_agent_api
import streamlit as st
from typing import List, Dict
from ui.utils.session_state import get_session_state, set_session_state
from ui.utils.conversation_handler import ConversationHandler

# Global variables
handler = ConversationHandler()
app = None  # Will be initialized later

def render_chat_interface():
    """Render the main chat interface"""
    global app  # Tell Python to use the global variable

    current_lead = get_session_state('current_lead')
    conversation_active = get_session_state('conversation_active')
    pending_input = get_session_state('pending_user_input')
    
    if not current_lead:
        st.warning("No lead selected")
        return
    
    st.markdown("### 💬 Conversation")
    
    chat_container = st.container()
    
    with chat_container:
        if app is None:
            app = get_agent_api(current_lead)
            set_session_state('agent_graph', app)
        
        conversation_history = get_session_state('conversation_history')
        if app.state is not None:
            conversation_history = app.state.get('messages', [])
        
        if conversation_history:
            for message in conversation_history:
                render_message(message)
        elif conversation_active:
            with st.spinner("Agent is preparing opening statement..."):
                try:
                    app.get_opening_statement(current_lead)
                    set_session_state('conversation_history', app.state['messages'])
                    st.rerun()
                except Exception as e:
                    st.error(f"Error starting conversation: {str(e)}")
        else:
            st.info("Click 'Start Conversation' in the sidebar to begin.")
    
    if conversation_active:
        render_user_input()
        if pending_input:
            # Process the agent response
            app = get_session_state('agent_graph')
            app.process_message(
                pending_input['lead_id'],
                pending_input['text']
            )
            
            set_session_state('conversation_history', app.state['messages'])
            set_session_state('pending_user_input', None)  # clear it
            st.rerun()  # Now rerun to show both messages
        if app.state['is_end']:
                conversation_active = False
                set_session_state('coversation_active', conversation_active)
                current_lead = None
                set_session_state('current_lead', current_lead)
                app = get_agent_api(current_lead)
                set_session_state('agent_graph', app)
                st.rerun()

def render_message(message: Dict):
    """Render a single message"""
    role = message['role']
    content = message['content']
    timestamp = message.get('timestamp', '')

    if role == 'agent':
        st.markdown(f"""
        <div class="agent-message">
            <strong>🤖 Zain (Sales Agent)</strong>
            <small style="float: right; color: gray;">{timestamp}</small>
            <br><br>
            {content}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="user-message">
            <strong>👤 You</strong>
            <small style="float: right; color: gray;">{timestamp}</small>
            <br><br>
            {content}
        </div>
        """, unsafe_allow_html=True)

def render_user_input():
    """Render user input section"""
    st.markdown("---")
    with st.form(key="user_input_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            user_input = st.text_area(
                "Your message:",
                placeholder="Type your response here...",
                height=100,
                key="user_message_input"
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            submit_button = st.form_submit_button("Send 📤", type="primary")
        
        if submit_button and user_input.strip():
            handle_user_input(user_input.strip())

def handle_user_input(user_input: str):
    """Handle user input and get agent response"""
    global handler  # Tell Python to use the global variable

    current_lead = get_session_state('current_lead')
    
    try:
        with st.spinner("Agent is thinking..."):
            handler.process_user_input(current_lead, user_input)  
        st.rerun()
    except Exception as e:
        st.error(f"Error processing message: {str(e)}")
        st.exception(e)  # For debugging
