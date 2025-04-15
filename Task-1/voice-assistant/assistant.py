# import speech_recognition as sr
# import pyttsx3
# import datetime
# import wikipedia
# import pywhatkit
# import webbrowser

# # Initialize the engine
# engine = pyttsx3.init()
# engine.setProperty('rate', 150)  # speaking speed

# # Speak function
# def speak(text):
#     engine.say(text)
#     engine.runAndWait()

# # Listen to microphone
# def listen():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         r.pause_threshold = 1
#         audio = r.listen(source)

#     try:
#         print("Recognizing...")
#         command = r.recognize_google(audio).lower()
#         print(f"You said: {command}")
#     except sr.UnknownValueError:
#         speak("Sorry, I didn't get that. Please say it again.")
#         return ""
#     return command

# # Main logic
# def run_assistant():
#     speak("Hello, I am your personal assistant. How can I help you today?")

#     while True:
#         command = listen()

#         if 'time' in command:
#             time = datetime.datetime.now().strftime('%I:%M %p')
#             speak(f"The time is {time}")

#         elif 'search' in command:
#             topic = command.replace('search', '')
#             result = wikipedia.summary(topic, sentences=2)
#             speak(result)

#         elif 'open youtube' in command:
#             webbrowser.open('https://www.youtube.com')
#             speak("Opening YouTube")

#         elif 'open google' in command:
#             webbrowser.open('https://www.google.com')
#             speak("Opening Google")

#         elif 'play' in command:
#             song = command.replace('play', '')
#             speak(f"Playing {song}")
#             pywhatkit.playonyt(song)

#         elif 'exit' in command or 'stop' in command:
#             speak("Goodbye!")
#             break

#         else:
#             speak("I didn't understand that. Please try again.")

# # Run the assistant
# run_assistant()


import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pywhatkit
import webbrowser
import requests
import platform
import os

# Initialize the engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # speaking speed

# Voice assistant name
ASSISTANT_NAME = "Peer"

# Speak function
def speak(text):
    print(f"{ASSISTANT_NAME}: {text}")
    engine.say(text)
    engine.runAndWait()

# Listen to microphone
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        command = r.recognize_google(audio).lower()
        print(f"You said: {command}")
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Please say it again.")
        return ""
    return command

# Get current weather (requires OpenWeatherMap API)
def get_weather(city="Delhi"):
    try:
        api_key = "your_openweathermap_api_key"  # Replace with your API key
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        if data.get("main"):
            temp = data['main']['temp']
            weather = data['weather'][0]['description']
            speak(f"The weather in {city} is {weather} with a temperature of {temp} degrees Celsius.")
        else:
            speak("Couldn't retrieve the weather right now.")
    except Exception as e:
        speak("There was a problem getting the weather.")

# System Info
def get_system_info():
    system = platform.system()
    release = platform.release()
    processor = platform.processor()
    speak(f"You are using {system} {release} with {processor} processor.")

# Main logic
def run_assistant():
    speak(f"Hello, I am {ASSISTANT_NAME}, your personal assistant. How can I help you today?")

    while True:
        command = listen()

        if not command:
            continue

        if 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            speak(f"The current time is {time}")

        elif 'date' in command:
            date = datetime.datetime.now().strftime('%A, %d %B %Y')
            speak(f"Today is {date}")

        elif 'weather' in command:
            speak("Which city do you want the weather for?")
            city = listen()
            get_weather(city)

        elif 'search' in command:
            topic = command.replace('search', '').strip()
            try:
                result = wikipedia.summary(topic, sentences=2)
                speak(result)
            except wikipedia.exceptions.DisambiguationError as e:
                speak("That topic is a bit broad. Can you be more specific?")
            except Exception as e:
                speak("Sorry, I couldn't find anything.")

        elif 'open youtube' in command:
            webbrowser.open('https://www.youtube.com')
            speak("Opening YouTube")

        elif 'open google' in command:
            webbrowser.open('https://www.google.com')
            speak("Opening Google")

        elif 'play' in command:
            song = command.replace('play', '').strip()
            speak(f"Playing {song}")
            pywhatkit.playonyt(song)

        elif 'system info' in command:
            get_system_info()

        elif 'shutdown' in command:
            speak("Shutting down the system.")
            os.system("shutdown /s /t 1")

        elif 'exit' in command or 'stop' in command:
            speak("Goodbye! Have a great day.")
            break

        else:
            speak("Sorry, I didn't understand that. Please try again.")

# Start the assistant
run_assistant()
