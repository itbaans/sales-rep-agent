import torch
from kokoro import KPipeline
import soundfile as sf
from playsound import playsound

class TextToSpeech:
    def __init__(self):
        self.engine = KPipeline(lang_code='a', device='cpu')

    def speak(self, text: str):
        # Generate speech audio
        generator = self.engine(text, voice='Kokoro-82M/voices/af_heart.pt')
        
        for i, (gs, ps, audio) in enumerate(generator):
            filename = f'{i}.wav'
            sf.write(filename, audio, 24000)
            print(f"Saved: {filename} | GS: {gs}, PS: {ps}")
            
            # Play audio immediately
            playsound(filename)


def main():
    tts = TextToSpeech()
    sample_text = "Hello there! This is a test of Kokoro text to speech."
    tts.speak(sample_text)


if __name__ == "__main__":
    main()
