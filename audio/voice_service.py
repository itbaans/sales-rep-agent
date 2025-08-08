import os
import subprocess
import time
import speech_recognition as sr

class VoiceService:
    
    def __init__(self):
        self._output_dir = "outputs"
        os.makedirs(self._output_dir, exist_ok=True)
    
    def listen(self):
        print('🎤 Listening (offline)...')
        try:
            # transcribed_file = os.path.join(self._output_dir, "transcribed-audio.wav")
            # r = sr.Recognizer()
            # with sr.Microphone(sample_rate=16000) as source:
            #     print("🧑 Say something...")
            #     audio = r.listen(source)

            # with open(transcribed_file, "wb") as f:
            #     f.write(audio.get_wav_data())

            start = time.time()
            output = self.process_audio("audio/test.wav")
            end = time.time()

            print('🕒 Transcribed in %.2f seconds' % (end - start))
            return output 
        except Exception as e:
            print(f"❌ Error during voice input: {e}")
            return None

    def process_audio(self, wav_file, model_name="base.en"):
        model_path = f"whisper.cpp/models/ggml-{model_name}.bin"

        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model not found at {model_path}\n"
                f"Download it using:\n\nbash ./models/download-ggml-model.sh {model_name}"
            )

        if not os.path.exists(wav_file):
            raise FileNotFoundError(f"WAV file not found: {wav_file}")

        full_command = f"whisper.cpp/build/bin/whisper-cli -m {model_path} -f {wav_file} -np -nt"
        process = subprocess.Popen(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if error and not output:
            raise Exception(f"Error processing audio: {error.decode('utf-8')}")

        return output.decode("utf-8").replace("[BLANK_AUDIO]", "").strip()
