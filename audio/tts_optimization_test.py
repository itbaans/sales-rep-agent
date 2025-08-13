import os
import numpy as np
import torch
import sounddevice as sd
import textwrap
import threading
from kokoro import KPipeline
import time

# CPU tuning
os.environ.setdefault("OMP_NUM_THREADS", "4")
os.environ.setdefault("MKL_NUM_THREADS", "4")
torch.set_num_threads(4)
torch.set_num_interop_threads(1)

class TextToSpeech:
    def __init__(self):
        self.engine = KPipeline(lang_code='a', device='cpu')
        self.sample_rate = 24000

    def _chunk_text(self, text, max_len=200):
        """Split text into manageable chunks for the model."""
        return textwrap.wrap(text, max_len, break_long_words=False)

    def _generate_audio(self, chunk, result_container):
        """Generate audio for a chunk."""
        with torch.inference_mode():
            generator = self.engine(chunk, voice='Kokoro-82M/voices/af_heart.pt')
        for _, (_, _, audio) in enumerate(generator):
            result_container.append(audio)

    def speak(self, text: str):
        chunks = self._chunk_text(text)

        # Generate first chunk before playback
        current_audio = []
        self._generate_audio(chunks[0], current_audio)

        for i in range(len(chunks)):
            # Start generating the next chunk while playing current one
            next_audio = []
            if i + 1 < len(chunks):
                gen_thread = threading.Thread(
                    target=self._generate_audio, args=(chunks[i+1], next_audio)
                )
                gen_thread.start()
            else:
                gen_thread = None

            # Play the current chunk
            sd.play(current_audio[0], self.sample_rate)
            sd.wait()

            # Wait for the next chunk to finish generating (if any)
            if gen_thread:
                gen_thread.join()
                current_audio = next_audio

def main():
    tts = TextToSpeech()
    while True:
        text = input("\n📝 Enter text (or 'q' to quit): ")
        if text.lower() == 'q':
            print("👋 Exiting...")
            break
        if text.strip():
            start_time = time.time()
            tts.speak(text)
            elapsed = time.time() - start_time
            print(f"✅ Inference complete in {elapsed:.2f} seconds.")

if __name__ == "__main__":
    main()
