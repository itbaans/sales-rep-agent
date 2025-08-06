import streamlit as st
import json
from pathlib import Path
from agent.services.memory_manager import load_memory

def render_lead_info(lead_id: str):
    """Render lead information panel"""
    
    # Load lead data
    leads_file = Path("data/leads.json")
    if not leads_file.exists():
        st.error("Leads file not found!")
        return
    
    with open(leads_file, 'r') as f:
        leads = json.load(f)
    
    lead_data = leads.get(lead_id, {})
    if not lead_data:
        st.error(f"Lead {lead_id} not found!")
        return
    
    # Lead information header
    with st.expander("📋 Lead Information", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"**Name:** {lead_data.get('name', 'N/A')}")
        
        with col2:
            st.markdown(f"**Company:** {lead_data.get('company', 'N/A')}")
        
        with col3:
            st.markdown(f"**Role:** {lead_data.get('role', 'N/A')}")
    
    # Lead memory and qualification info
    render_lead_memory_summary(lead_id)

def render_lead_memory_summary(lead_id: str):
    """Render lead memory and qualification summary"""
    
    memory = load_memory(lead_id)
    
    if memory and memory.get('detailed_memory'):
        detailed = memory['detailed_memory']
        
        with st.expander("🎯 Lead Qualification & Status"):
            # Qualification scores
            if detailed.get('lead_qualification_score'):
                st.markdown("**Qualification Score:**")
                scores = detailed['lead_qualification_score']
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Budget Fit", f"{scores.get('budget_fit', 0)}/10")
                with col2:
                    st.metric("Authority", f"{scores.get('authority_level', 0)}/10")
                with col3:
                    st.metric("Need Urgency", f"{scores.get('need_urgency', 0)}/10")
                with col4:
                    st.metric("Engagement", f"{scores.get('engagement_level', 0)}/10")
            
            # Conversation stage and sentiment
            col1, col2 = st.columns(2)
            with col1:
                stage = detailed.get('conversation_stage_reached', 'Unknown')
                st.markdown(f"**Stage:** `{stage.title()}`")
            
            with col2:
                sentiment = detailed.get('overall_sentiment', 'Unknown')
                sentiment_emoji = {
                    'Positive': '😊',
                    'Neutral': '😐',
                    'Negative': '😞',
                    'Mixed': '🤔'
                }.get(sentiment, '❓')
                st.markdown(f"**Sentiment:** {sentiment_emoji} {sentiment}")
            
            # Buying signals and objections
            col1, col2 = st.columns(2)
            
            with col1:
                if detailed.get('buying_signals_detected'):
                    st.markdown("**🟢 Buying Signals:**")
                    for signal in detailed['buying_signals_detected']:
                        st.markdown(f"• {signal}")
            
            with col2:
                if detailed.get('objections_raised'):
                    st.markdown("**🔴 Objections:**")
                    for objection in detailed['objections_raised']:
                        st.markdown(f"• {objection}")
            
            # Next steps and follow-up
            if detailed.get('next_steps_agreed') or detailed.get('follow_up_timing'):
                st.markdown("**📅 Next Steps:**")
                
                if detailed.get('next_steps_agreed'):
                    for step in detailed['next_steps_agreed']:
                        st.markdown(f"• {step}")
                
                if detailed.get('follow_up_timing'):
                    st.markdown(f"**Follow-up timing:** {detailed['follow_up_timing']}")
    
    else:
        with st.expander("🎯 Lead Qualification & Status"):
            st.info("No qualification data available yet. Start a conversation to gather information.")

def render_conversation_insights(lead_id: str):
    """Render additional conversation insights"""
    
    memory = load_memory(lead_id)
    
    if memory and memory.get('detailed_memory'):
        detailed = memory['detailed_memory']
        
        # Show pain points and interests
        if detailed.get('key_pain_points_confirmed') or detailed.get('solutions_of_interest'):
            with st.expander("🎯 Business Insights"):
                
                if detailed.get('key_pain_points_confirmed'):
                    st.markdown("**Pain Points:**")
                    for pain in detailed['key_pain_points_confirmed']:
                        st.markdown(f"• {pain}")
                
                if detailed.get('solutions_of_interest'):
                    st.markdown("**Solutions of Interest:**")
                    for solution in detailed['solutions_of_interest']:
                        st.markdown(f"• {solution}")
                
                if detailed.get('projects_of_interest'):
                    st.markdown("**Projects of Interest:**")
                    for project in detailed['projects_of_interest']:
                        st.markdown(f"• {project}")