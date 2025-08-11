from audio.voice_service import VoiceService
from audio.tts import TextToSpeech  # Assuming you're using pyttsx3
from agent.AgentAPI import get_agent_api 

def main():
    lead_id = "lead_2024_0156"
    agent_api = get_agent_api(lead_id=lead_id)
    
    if not agent_api.initialize_knowledge():
        print("❌ Failed to initialize knowledge bases!")
        return

    # Init voice input/output
    voice = VoiceService()
    tts = TextToSpeech()

    print("\n" + "="*50)
    opening = agent_api.get_opening_statement(lead_id)
    print(f"🤖 Agent: {opening}")
    tts.speak(opening)
    print("="*50)

    while True:
        try:
            user_input = voice.listen()
            if not user_input:
                continue

            print(f"\n🧑 You said: {user_input}")

            print("\n🤔 [Agent is thinking...]")
            response = agent_api.process_message(lead_id, user_input)

            print(f"\n🤖 Agent: {response}")
            #tts.speak(response)
            print("-" * 50)

            if agent_api.state.get('is_end', False):
                break

        except KeyboardInterrupt:
            print("\n\n🛑 Conversation stopped by user.")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            break

if __name__ == "__main__":
    main()