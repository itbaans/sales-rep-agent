import socket
import json
from audio.voice_service import VoiceService# your existing VoiceService class

HOST = '127.0.0.1'
PORT = 5001

def run_server():
    
    vs = VoiceService()
    print(f"🎤 Voice Service listening on {HOST}:{PORT}...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        print(f"✅ Connected to {addr}")

        with conn:
            buffer = ""
            while True:
                chunk = conn.recv(1024).decode('utf-8')
                if not chunk:
                    break

                buffer += chunk
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    try:
                        msg = json.loads(line)
                        command = msg.get("command")

                        if command == "listen":
                            print("🎙️ Starting recording...")
                            text = vs.listen()
                            response = json.dumps({"transcription": text})
                            conn.sendall(response.encode('utf-8') + b"\n")

                        elif command == "quit":
                            print("❌ Closing connection")
                            return

                    except json.JSONDecodeError:
                        continue

if __name__ == "__main__":
    run_server()
