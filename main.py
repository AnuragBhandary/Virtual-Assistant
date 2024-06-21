import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import google.generativeai as genai
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def aiProcess(command):
    genai.configure(api_key='''YOUR GEMINI API KEY''')

    model = genai.GenerativeModel('gemini-1.5-flash')

    response = model.generate_content(command + ". Give a short answer")
    return response.text

def processCommand(c):
    print(c)
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    else:
        # Let openAI handle the request
        output = aiProcess(c)    
        speak(output)    

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        # Listen for the wake word "Jarvis"
        # Obtain audio from the microphone
        r = sr.Recognizer()

        # Recognize speech using Google
        try:
            with sr.Microphone() as source:
                print("Listening....")
                audio = r.listen(source, timeout = 2, phrase_time_limit = 1)
            word = r.recognize_google(audio)
            print(word)
            if(word.lower() == "jarvis stop"):
                speak("Ending assistance")
                quit()
            elif(word.lower() == "jarvis"):
                speak("Yeah")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active....")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)
            
        
        except Exception as e:
            print("Error; {0}".format(e))
