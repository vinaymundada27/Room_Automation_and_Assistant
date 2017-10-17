# Requires PyAudio and PySpeech.

import speech_recognition as sr
from gtts import gTTS
import os
from smart_agent import smart_agent_answer
import settings


####### GLOBAL PARAMETERS #############
HELLO_BUDDY = False

# Record Audio
recognizer = sr.Recognizer()

def speak(TEXT):
    tts = gTTS(text=TEXT, lang='en')
    tts.save("text.mp3")
    os.system("mpg123 text.mp3")


def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
        print("recorded")

    # Speech recognition using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)
        text = recognizer.recognize_google(audio)
        print("You said : " + text)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return None


def handle_action(ans):

    ## CHANGE THE GLOBAL PARAMETERS ###
    ind = settings.labels.index(ans)

    # lights
    if ind < 4:
        settings.LIGHT_AUTOMATION_OFF = False
        if ind < 2:
            settings.LIGHT_FREQ_FALSE = settings.MIN
            settings.LIGHT_FREQ_TRUE = settings.MAX

        elif ind > 2 and ind < 4:
            settings.LIGHT_FREQ_TRUE = settings.MIN
            settings.LIGHT_FREQ_FALSE = settings.MAX
            
    else:
        # fan
        settings.FAN_AUTOMATION_OFF = False
        if ind > 3 and ind < 6:
            settings.FAN_FREQ_FALSE = settings.MIN
            settings.FAN_FREQ_TRUE = settings.MAX

        elif ind > 5 and ind < 8:
            settings.FAN_FREQ_TRUE = settings.MIN
            settings.FAN_FREQ_FALSE = settings.MAX
    

def start_listening():	
    while True:
	speak("Hello Geetha Ma'am. How can I help you?")
	voice = listen()
	if voice:
	    speak("You said " + voice)

	    ###### SMART AGENT ########
	    ans = smart_agent_answer(voice)

            if ans in settings.labels:
                print ans
                handle_action(ans)

            # Bing reply
	    else:
                print ans
                speak(ans)
	else:
            speak("Could not hear")



def keep_listening():
    while True:
	voice = listen()
	if voice:
	    print("you said : " + voice)
            if voice == "hello buddy":
		global HELLO_BUDDY
		HELLO_BUDDY = True
		start_listening()
	    else:
		print("no hello buddy")
	else:
	    print("continue")


#keep_listening()
