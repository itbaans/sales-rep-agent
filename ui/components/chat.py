import streamlit as st
from typing import List, Dict
from ui.utils.session_state import get_session_state, set_session_state
from ui.utils.conversation_handler import ConversationHandler

def render_chat_interface():
    """Render the main chat interface"""
    
    current_lead = get_session_state('current_lead')
    conversation_active = get_session_state('conversation_active')
    
    if not current_lead:
        st.warning("No lead selected")
        return
    
    st.markdown("### 💬 Conversation")
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        conversation_history = get_session_state('conversation_history', [])
        
        # Display conversation history
        if conversation_history:
            for message in conversation_history:
                render_message(message)
        elif conversation_active:
            # If conversation is active but no history, start with agent's opening
            with st.spinner("Agent is preparing opening statement..."):
                try:
                    handler = ConversationHandler()
                    opening_message = handler.start_conversation(current_lead)
                    
                    # Add to history
                    conversation_history.append({
                        'role': 'agent',
                        'content': opening_message,
                        'timestamp': handler.get_current_timestamp()
                    })
                    set_session_state('conversation_history', conversation_history)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error starting conversation: {str(e)}")
        else:
            st.info("Click 'Start Conversation' in the sidebar to begin.")
    
    # User input
    if conversation_active:
        render_user_input()

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
    
    # Create a form for user input
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
            st.markdown("<br>", unsafe_allow_html=True)  # Add some space
            submit_button = st.form_submit_button("Send 📤", type="primary")
        
        if submit_button and user_input.strip():
            handle_user_input(user_input.strip())

def handle_user_input(user_input: str):
    """Handle user input and get agent response"""
    
    current_lead = get_session_state('current_lead')
    conversation_history = get_session_state('conversation_history', [])
    
    try:
        handler = ConversationHandler()
        
        # Add user message to history
        user_message = {
            'role': 'user',
            'content': user_input,
            'timestamp': handler.get_current_timestamp()
        }
        conversation_history.append(user_message)
        
        # Show processing
        with st.spinner("Agent is thinking..."):
            # Get agent response
            agent_response = handler.process_user_input(current_lead, user_input, conversation_history)
            
            # Add agent response to history
            agent_message = {
                'role': 'agent',
                'content': agent_response,
                'timestamp': handler.get_current_timestamp()
            }
            conversation_history.append(agent_message)
            
        # Update session state
        set_session_state('conversation_history', conversation_history)
        
        # Rerun to show new messages
        st.rerun()
        
    except Exception as e:
        st.error(f"Error processing message: {str(e)}")
        st.exception(e)  # For debugging