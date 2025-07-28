from langgraph.graph import StateGraph, END
from agent.state import ConversationState
from agent.nodes import data_retrieval, interaction, routing, tools, finalization

def create_agent_graph() -> StateGraph:
    """Builds the LangGraph agent."""
    workflow = StateGraph(ConversationState)

    # Add nodes
    workflow.add_node("retrieve_lead_data", data_retrieval.retrieve_lead_data)
    workflow.add_node("retrieve_company_data", data_retrieval.retrieve_company_data)
    workflow.add_node("generate_initial_prompt", interaction.generate_initial_prompt)
    workflow.add_node("generate_response", interaction.generate_response)
    workflow.add_node("retrieve_from_knowledge_base", tools.retrieve_from_knowledge_base)
    workflow.add_node("update_conversation_summary", finalization.update_conversation_summary)
    workflow.add_node("update_lead_insights", finalization.update_lead_insights)
    workflow.add_node("update_next_actions", finalization.update_next_actions)
    workflow.add_node("process_user_response", interaction.process_user_response)

    # Set entry point and build edges
    workflow.set_entry_point("retrieve_lead_data")
    workflow.add_edge("retrieve_lead_data", "retrieve_company_data")
    workflow.add_edge("retrieve_company_data", "generate_initial_prompt")

    workflow.add_edge("generate_initial_prompt", "process_user_response")
    
    
    # This is the main interactive part. After each agent response, we wait for user input.
    # The router then decides where to go next.
    workflow.add_conditional_edges(
        "process_user_response", # The source node will be where the conversation loop starts
        routing.router,
        {
            "retrieve_from_knowledge_base": "retrieve_from_knowledge_base",
            "generate_response": "generate_response",
            "end_conversation": "update_conversation_summary",
        }
    )
    workflow.add_edge("retrieve_from_knowledge_base", "generate_response")
    workflow.add_edge("generate_response", "process_user_response")

    # Finalization flow
    workflow.add_edge("update_conversation_summary", "update_lead_insights")
    workflow.add_edge("update_lead_insights", "update_next_actions")
    workflow.add_edge("update_next_actions", END)

    return workflow.compile()