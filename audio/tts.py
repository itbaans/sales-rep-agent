import os
import time
import torch
from kokoro import KPipeline
import soundfile as sf
from playsound import playsound

class TextToSpeech:
    def __init__(self):
        self.engine = KPipeline(lang_code='a', device='cpu')
        self.output_dir = "tts_outputs"
        os.makedirs(self.output_dir, exist_ok=True)
        self.counter = 0

    def speak(self, text: str):
        # Generate speech audio
        generator = self.engine(text, voice='Kokoro-82M/voices/af_heart.pt')
        
        for _, (gs, ps, audio) in enumerate(generator):
            filename = os.path.join(self.output_dir, f"{self.counter}_{int(time.time()*1000)}.wav")
            sf.write(filename, audio, 24000)
            print(f"💾 Saved: {filename} | GS: {gs}, PS: {ps}")
            
            # Play audio immediately
            playsound(filename)

            self.counter += 1
