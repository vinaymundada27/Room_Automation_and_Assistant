from gtts import gTTS
import os

def speak(TEXT):
    tts = gTTS(text=TEXT, lang='en')
    tts.save("text.mp3")
    os.system("mpg123 text.mp3")


speak("Good morning")
