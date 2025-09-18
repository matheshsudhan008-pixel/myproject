import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import random

# Initialize text-to-speech
engine = pyttsx3.init()
engine.setProperty("rate", 170)  # Speed
engine.setProperty("volume", 1.0)  # Volume
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)  # Female voice

def speak(text):
    print("🤖 Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language="en-in")
        print(f"👂 You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Please repeat.")
        return ""
    except sr.RequestError:
        speak("Network error. Try again later.")
        return ""

def wish_me():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good morning!")
    elif hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am your AI assistant. How can I help you today?")

def run_ai():
    wish_me()
    while True:
        query = listen()

        if "time" in query:
            str_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {str_time}")

        elif "date" in query:
            str_date = datetime.datetime.now().strftime("%A, %d %B %Y")
            speak(f"Today's date is {str_date}")

        elif "open youtube" in query:
            webbrowser.open("https://www.youtube.com")
            speak("Opening YouTube")

        elif "open google" in query:
            webbrowser.open("https://www.google.com")
            speak("Opening Google")

        elif "play music" in query:
            music_dir = "C:\\Users\\Public\\Music"  # Change path to your music folder
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, random.choice(songs)))
            speak("Playing music for you")

        elif "quit" in query or "exit" in query:
            speak("Goodbye! Have a great day.")
            break

        elif query:
            # Default response if no command matched
            speak("I can’t do that yet, but I’m learning!")

if __name__ == "__main__":
    run_ai()
