# main.py

import pprint
from agent.graph import create_agent_graph

app = create_agent_graph()

def run_conversation():
    lead_id = "lead_2024_0156"
    config = {"configurable": {"thread_id": lead_id}}

    # 1. Kick off the graph to get the agent's opening statement.
    # No user_input is provided here, which is the correct starting state.
    initial_state = {"lead_id": lead_id}
    current_state = app.invoke(initial_state, config)
    
    # print(f"\nAgent: {current_state['messages'][-1]['content']}\n")

    # # 2. Enter the interactive loop where the user is always the next to speak.
    # while True:
    #     user_input = input("Your response: ")
    #     if "exit" in user_input.lower():
    #         print("Ending session.")
    #         break
        
    #     # Prepare state for the next turn. This state already contains the agent's
    #     # first message and will now include the user's first reply.
    #     current_state['user_input'] = user_input
    #     current_state['messages'].append({"role": "user", "content": user_input})
    #     current_state['scratchpad'] = []
    #     current_state['retrieved_docs'] = []

    #     # Invoke the graph. The router will now see that `messages` is not empty
    #     # and will correctly route to the `think` node.
    #     result_state = app.invoke(current_state, config)

    #     if result_state.get('messages') and len(result_state['messages']) > len(current_state['messages']):
    #         print(f"\nAgent: {result_state['messages'][-1]['content']}\n")
    #     else:
    #         print("\n---Conversation Concluded by Agent. Final State---")
    #         pprint.pprint(result_state)
    #         break
        
    #     # The output of this turn becomes the input for the next
    #     current_state = result_state

if __name__ == "__main__":
    run_conversation()