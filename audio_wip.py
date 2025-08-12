import socket
import json
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
from audio.tts import TextToSpeech
from agent.AgentAPI import get_agent_api

HOST = '127.0.0.1'
PORT = 5001

def main():
    lead_id = "lead_2024_0156"
    agent_api = get_agent_api(lead_id=lead_id)
    tts = TextToSpeech()

    if not agent_api.initialize_knowledge():
        print("❌ Failed to initialize knowledge bases!")
        return

    # Connect to Voice Service
    print(f"🔌 Connecting to Voice Service at {HOST}:{PORT}...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print("✅ Connected!")

    opening = agent_api.get_opening_statement(lead_id)
    print(f"🤖 Agent: {opening}")
    tts.speak(opening)

    try:
        buffer = ""
        while True:
            # Tell voice service to start listening
            sock.sendall(json.dumps({"command": "listen"}).encode('utf-8') + b"\n")

            # Wait for transcription
            while True:
                chunk = sock.recv(1024).decode('utf-8')
                if not chunk:
                    return
                buffer += chunk
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    try:
                        msg = json.loads(line)
                        if "transcription" in msg:
                            user_input = msg["transcription"]
                            print(f"\n🧑 You said: {user_input}")
                            print("\n🤔 [Agent is thinking...]")
                            response = agent_api.process_message(lead_id, user_input)
                            print(f"\n🤖 Agent: {response}")
                            tts.speak(response)  # After speaking, go to next listen loop
                            if agent_api.state.get('is_end', False):
                                sock.sendall(json.dumps({"command": "quit"}).encode('utf-8') + b"\n")
                                return
                            break
                    except json.JSONDecodeError:
                        continue
                else:
                    continue
                break  # Exit inner loop and send next "listen"

    except KeyboardInterrupt:
        print("\n🛑 Conversation stopped by user.")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
