# Importing required libraries
# These handle voice input/output, web access, AI responses, system info, and APIs
import speech_recognition as sr
import webbrowser
import pyttsx3
from musicLibrary import music  # Custom music library with song links
import openai
from gtts import gTTS
import pygame
import os
import datetime
import psutil
import requests
from dotenv import load_dotenv
import time

# Load API keys securely from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
newsapi = os.getenv("NEWS_API_KEY")
weatherapi = os.getenv("WEATHER_API_KEY")

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Store short-term conversation memory to provide context for AI responses
conversation_history = [
    {"role": "system", "content": "You are Leo, a helpful and intelligent virtual assistant like Jarvis."}
]

# Function to speak text using gTTS (Google Text-to-Speech) with pygame fallback
def speak(text):
    try:
        tts = gTTS(text)
        filename = "temp.mp3"
        tts.save(filename)
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        # Fallback to pyttsx3 if gTTS fails (no internet etc.)
        print(f"TTS error: {e}")
        engine.say(text)
        engine.runAndWait()
    finally:
        if os.path.exists("temp.mp3"):
            pygame.mixer.music.unload()
            os.remove("temp.mp3")

# Function to get weather using OpenWeatherMap API
def get_weather(city):
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return "Weather API key not found. Please check your .env file."

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    print(f"Weather API URL: {url}")

    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print("Raw Response:", response.text)

        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            return f"The current temperature in {city} is {temp}°C with {desc}."
        else:
            return f"Sorry, couldn't fetch weather. Error: {response.status_code} - {response.reason}"
    except requests.exceptions.RequestException as e:
        return f"Weather request failed: {e}"

# Function to handle AI-based responses using OpenAI's GPT-3.5 model
def aiProcess(command):
    try:
        conversation_history.append({"role": "user", "content": command})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history
        )
        reply = response.choices[0].message["content"]
        conversation_history.append({"role": "assistant", "content": reply})
        return reply
    except Exception as e:
        return f"Sorry, I couldn't process your request: {e}"

# Get battery status and current system time
def get_system_info():
    battery = psutil.sensors_battery()
    percent = battery.percent if battery else 'unknown'
    plugged = battery.power_plugged if battery else False
    time_str = datetime.datetime.now().strftime("%I:%M %p on %A")
    return f"Battery at {percent} percent, plugged in: {plugged}. The time is {time_str}."

# Function to return a random tech-related joke
def tell_joke():
    jokes = [
        "Why don’t scientists trust atoms? Because they make up everything!",
        "Why did the computer get cold? Because it forgot to close Windows.",
        "I told my computer I needed a break, and now it won’t stop sending me KitKat ads."
    ]
    return jokes[datetime.datetime.now().second % len(jokes)]

# Core function that maps voice commands to actions
def processCommand(c):
    c = c.lower()
    if "open" in c:
        # Opening websites based on keywords
        if "google" in c:
            webbrowser.open("https://google.com")
        elif "instagram" in c:
            webbrowser.open("https://www.instagram.com/")
        elif "youtube" in c:
            webbrowser.open("https://www.youtube.com/")
        elif "linkedin" in c:
            webbrowser.open("https://www.linkedin.com/")
        elif "facebook" in c:
            webbrowser.open("https://www.facebook.com/")
        elif "leetcode" in c:
            webbrowser.open("https://www.leetcode.com/")
        elif "striver" in c:
            webbrowser.open("https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/")
        else:
            speak("I couldn't recognize the site you wanted to open.")
    elif "play" in c:
        # Playing music from the predefined library
        try:
            words = c.split()
            song_name = " ".join(words[1:]).strip().title()
            if song_name in music:
                speak(f"Playing {song_name}")
                webbrowser.open(music[song_name])
            else:
                speak(f"Sorry, I couldn't find {song_name} in your music library.")
        except:
            speak("Something went wrong while playing music.")
    elif "weather" in c:
        # Fetch weather report (city currently fixed as Kolkata)
        city = "Kolkata"
        weather_report = get_weather(city)
        speak(weather_report)
    elif "time" in c or "battery" in c:
        # Speak system info
        info = get_system_info()
        speak(info)
    elif "joke" in c:
        speak(tell_joke())
    elif "news" in c:
        # Read top 5 news headlines using NewsAPI
        if not newsapi:
            speak("News API key not found. Please check your .env file.")
            return
        url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                articles = data.get("articles", [])[:5]
                if not articles:
                    speak("Sorry, I couldn't find any news right now.")
                else:
                    speak("Here are the top news headlines:")
                    for article in articles:
                        speak(article["title"])
            else:
                speak(f"Sorry, I couldn't fetch news. Error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            speak(f"News request failed: {e}")
    elif any(word in c for word in ["exit", "quit", "goodbye", "stop"]):
        # Graceful exit on voice command
        speak("Goodbye! Shutting down now.")
        exit()
    else:
        # AI handles generic or undefined commands
        output = aiProcess(c)
        speak(output)

# MAIN LOOP — voice-controlled trigger word detection and execution
if __name__ == "__main__":
    speak("Initializing Leo...")
    while True:
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            word = recognizer.recognize_google(audio).lower()
            if word == "leo":
                speak("Yes?")
                with sr.Microphone() as source:
                    print("Listening for command...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
                    command = recognizer.recognize_google(audio)
                    print("Command:", command)
                    processCommand(command)
            time.sleep(1)  # Prevent CPU overload
        except Exception as e:
            print("Error:", e)
            time.sleep(1)
