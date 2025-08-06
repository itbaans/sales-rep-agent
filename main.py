import pprint
import sys
from agent.graph import create_agent_graph
from IPython.display import Image, display
from vectorstores.create_knowledge_bases import initialize_vector_knowledge, initialize_json_knowledge

def visualize_graph():
    """Generate graph visualization"""
    app = create_agent_graph()
    with open("agent_graph.png", "wb") as f:
        f.write(app.get_graph(xray=True).draw_mermaid_png())
    print("Graph visualization saved as 'agent_graph.png'")

def run_cli_conversation():
    """Run the original CLI conversation mode"""
    app = create_agent_graph()
    lead_id = "lead_2024_0156"
    config = {"configurable": {"thread_id": lead_id}}

    # Initialize knowledge bases
    print("Initializing knowledge bases...")
    initialize_vector_knowledge()
    initialize_json_knowledge()
    print("Knowledge bases initialized!")

    # 1. Kick off the graph to get the agent's opening statement.
    initial_state = {"lead_id": lead_id}
    app.invoke(initial_state, config)

def run_streamlit():
    """Run the Streamlit UI version"""
    import subprocess
    subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "streamlit":
            print("Starting Streamlit UI...")
            run_streamlit()
        elif sys.argv[1] == "cli":
            print("Starting CLI conversation...")
            run_cli_conversation()
        elif sys.argv[1] == "graph":
            print("Generating graph visualization...")
            visualize_graph()
        else:
            print("Usage: python main.py [streamlit|cli|graph]")
    else:
        # Default to CLI for backward compatibility
        print("Starting CLI conversation... (use 'python main.py streamlit' for UI)")
        run_cli_conversation()