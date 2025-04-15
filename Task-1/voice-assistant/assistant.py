import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pywhatkit
import webbrowser
import requests
import platform
import os
import re
import operator

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
        api_key = "your_openweathermap_api_key"  # Replace with your API key or disable weather functionality if you don't have one
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

# Math Operations Functionality
# Define mapping of word-based math keywords to operator functions
ops = {
    'plus': operator.add,
    'add': operator.add,
    'minus': operator.sub,
    'subtract': operator.sub,
    'times': operator.mul,
    'multiply': operator.mul,
    'divided by': operator.truediv,
    'divide': operator.truediv
}

def perform_math_operation(command):
    try:
        # First, check for word-based operators
        for word, op_func in ops.items():
            if word in command:
                parts = re.split(word, command)
                if len(parts) == 2:
                    numbers1 = re.findall(r'\d+(?:\.\d+)?', parts[0])
                    numbers2 = re.findall(r'\d+(?:\.\d+)?', parts[1])
                    if numbers1 and numbers2:
                        num1 = float(numbers1[-1])
                        num2 = float(numbers2[0])
                        result = op_func(num1, num2)
                        speak(f"The result is {result}")
                        return

        # Next, check for symbol-based operators
        symbol_ops = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv
        }
        for symbol, op_func in symbol_ops.items():
            if symbol in command:
                parts = command.split(symbol)
                if len(parts) == 2:
                    numbers1 = re.findall(r'\d+(?:\.\d+)?', parts[0])
                    numbers2 = re.findall(r'\d+(?:\.\d+)?', parts[1])
                    if numbers1 and numbers2:
                        num1 = float(numbers1[-1])
                        num2 = float(numbers2[0])
                        result = op_func(num1, num2)
                        speak(f"The result is {result}")
                        return
        speak("Sorry, I couldn't understand the math operation.")
    except Exception as e:
        speak("There was an error while calculating.")

# Main logic
def run_assistant():
    speak(f"Hello, I am {ASSISTANT_NAME}, your personal assistant. How can I help you today?")

    while True:
        command = listen()

        if not command:
            continue

        if 'time' in command:
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            speak(f"The current time is {current_time}")

        elif 'date' in command:
            current_date = datetime.datetime.now().strftime('%A, %d %B %Y')
            speak(f"Today is {current_date}")

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

        # Check for math operations from words or symbol syntax
        elif any(op in command for op in list(ops.keys()) + ['+', '-', '*', '/']):
            perform_math_operation(command)

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
