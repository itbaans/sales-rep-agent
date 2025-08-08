import pprint
import sys
from agent.graph import create_agent_graph
from IPython.display import Image, display
from vectorstores.create_knowledge_bases import initialize_vector_knowledge, initialize_json_knowledge
from agent.AgentAPI import get_agent_api

def visualize_graph():
    """Generate graph visualization"""
    app = create_agent_graph()
    with open("agent_graph.png", "wb") as f:
        f.write(app.get_graph(xray=True).draw_mermaid_png())
    print("Graph visualization saved as 'agent_graph.png'")

def run_cli_conversation():
    """Run CLI conversation using the new API"""
    lead_id = "lead_2024_0156"
    agent_api = get_agent_api(lead_id=lead_id)
    # Initialize knowledge bases
    if not agent_api.initialize_knowledge():
        print("Failed to initialize knowledge bases!")
        return
    
    # Get opening statement
    print("\n" + "="*50)
    opening = agent_api.get_opening_statement(lead_id)
    print(f"Agent: {opening}")
    print("="*50)
    
    # Conversation history for context
    
    # CLI loop
    while True:
        try:
            user_input = input("\nYour response: ").strip()
            
            if not user_input:
                continue
                
            print("\n[Agent is thinking...]")
            response = agent_api.process_message(lead_id, user_input)
            
            print(f"\nAgent: {response}")
            print("-" * 50)

            if agent_api.state.get('is_end', False):
                break
            
        except KeyboardInterrupt:
            print("\n\nConversation ended.")
            break
        except Exception as e:
            print(f"\nError: {e}")
            break

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