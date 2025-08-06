import pprint
from agent.graph import create_agent_graph
from IPython.display import Image, display
from vectorstores.create_knowledge_bases import initialize_vector_knowledge, initialize_json_knowledge

app = create_agent_graph()

def visualize_graph():
    with open("agent_graph.png", "wb") as f:
        f.write(app.get_graph(xray=True).draw_mermaid_png())

def run_conversation():
    lead_id = "lead_2024_0156"
    config = {"configurable": {"thread_id": lead_id}}

    # 1. Kick off the graph to get the agent's opening statement.
    # No user_input is provided here, which is the correct starting state.
    initial_state = {"lead_id": lead_id}
    app.invoke(initial_state, config)


if __name__ == "__main__":
    initialize_vector_knowledge()
    initialize_json_knowledge()
    run_conversation()
    #visualize_graph()