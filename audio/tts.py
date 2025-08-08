import pyttsx3

class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 160)  # speed
        self.engine.setProperty("volume", 1.0)  # max volume

    def speak(self, text: str):
        self.engine.say(text)
        self.engine.runAndWait()
