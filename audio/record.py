import sounddevice as sd
import soundfile as sf

def record_audio(filename='audio.wav', duration=5, samplerate=16000):
    print("🎤 Recording... Speak now")
    audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1)
    sd.wait()
    sf.write(filename, audio, samplerate)
    print("✅ Recording saved.")
