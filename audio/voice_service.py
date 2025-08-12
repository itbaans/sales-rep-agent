import os
import queue
import sys
import threading
import time
import sounddevice as sd
import soundfile as sf
import subprocess

class VoiceService:
    def __init__(self):
        self._output_dir = "outputs"
        os.makedirs(self._output_dir, exist_ok=True)
        self._whisper_exe = r"whisper.cpp\whisper-cli.exe"  # Windows executable path
        self._model_dir = r"whisper.cpp\models"
        self._samplerate = 16000
        self._channels = 1
        self._q = queue.Queue()

    def _callback(self, indata, frames, time_info, status):
        """Callback from sounddevice, put recorded data into a queue."""
        if status:
            print(status, file=sys.stderr)
        # Always ensure indata is (frames, channels)
        self._q.put(indata.copy())

    def listen(self):
        """
        Records until Enter is pressed, then transcribes with whisper.cpp
        """
        temp_wav = os.path.join(self._output_dir, "mic_input.wav")
        print("🎤 Recording... press ENTER to stop")

        # Thread for stopping on Enter
        stop_event = threading.Event()
        threading.Thread(target=lambda: (input(), stop_event.set()), daemon=True).start()

        # Start recording
        with sf.SoundFile(temp_wav, mode='w', samplerate=self._samplerate,
                          channels=self._channels, subtype='PCM_16') as file:
            with sd.InputStream(samplerate=self._samplerate, channels=self._channels,
                                callback=self._callback):
                while not stop_event.is_set():
                    file.write(self._q.get())

        print("✅ Recording stopped, transcribing...")
        start = time.time()
        text = self.process_audio(temp_wav)
        end = time.time()
        print(f"🕒 Transcribed in {end - start:.2f} seconds")
        return text

    def process_audio(self, wav_file, model_name="base.en"):
        """Run whisper.cpp CLI to transcribe audio."""
        model_path = os.path.join(self._model_dir, f"ggml-{model_name}.bin")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found: {model_path}")
        if not os.path.exists(wav_file):
            raise FileNotFoundError(f"WAV file not found: {wav_file}")

        cmd = [
            self._whisper_exe,
            "-m", model_path,
            "-f", wav_file,
            "-np", "-nt"
        ]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if process.returncode != 0:
            raise RuntimeError(f"Whisper error: {error.decode('utf-8')}")

        return output.decode("utf-8").replace("[BLANK_AUDIO]", "").strip()


# if __name__ == "__main__":
#     vs = VoiceService()
#     text = vs.listen()
#     print("\n📝 Transcription:", text)
