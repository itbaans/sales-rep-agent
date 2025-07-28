import pprint
from agent.graph import create_agent_graph
from agent.state import ConversationState

app = create_agent_graph()

def run_conversation():
    lead_id = "lead_2024_0156"
    initial_state: ConversationState = {
        "lead_id": lead_id,
        "messages": [],
        # All other fields are optional and will be populated by the graph
        "user_input": None,
        "lead_data": {},
        "company_data": {},
        "conversation_summary": None,
        "lead_insights": None,
        "next_actions": None,
    }

    # Start the conversation
    config = {"configurable": {"thread_id": lead_id}}
    current_state = app.invoke(initial_state, config)
    
    agent_message = current_state['messages'][-1]['content']
    print(f"\nAgent: {agent_message}\n")

    # Interactive loop
    while True:
        user_input = input("Your response: ")
        
        current_state['user_input'] = user_input
        current_state['messages'].append({"role": "user", "content": user_input})

        # Invoke the graph with the new user input
        current_state = app.invoke(current_state, config)
        
        # Check if the graph has finished
        if not current_state:
             # The final state might be empty if the graph hit the END node immediately.
             # You may need to retrieve the final state from your persistence layer if you add one.
            print("\n---Conversation Ended---")
            # To get the final state before it ends, you would need to inspect the stream of events
            # For simplicity, we assume the last valid state holds the summary.
            break

        agent_message = current_state['messages'][-1]['content']
        print(f"\nAgent: {agent_message}\n")

        # A simple check to break the loop if the conversation is flagged to end
        if "bye" in user_input.lower() or "thank you" in user_input.lower():
            final_state = app.invoke(current_state, config) # Run finalization steps
            print("\n---FINAL LEAD STATE---")
            pprint.pprint(final_state)
            break


if __name__ == "__main__":
    run_conversation()