from whisper_cpp_python import Whisper

class SpeechToText:
    def __init__(self, model_path="./models/ggml-base.en.bin"):
        self.whisper = Whisper(model_path)

    def transcribe(self, file_path: str) -> str:
        result = self.whisper.transcribe(file_path)
        return result["text"]
