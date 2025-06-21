🤖 Leo – Your Personal AI Virtual Assistant

Leo is a smart voice-activated virtual assistant written in Python. Inspired by Iron Man’s JARVIS, Leo can listen to voice commands, respond with intelligent answers using OpenAI, play music, fetch the latest weather and news, open websites, tell jokes, and more!

🚀 Features

- 🎤 Voice Recognition – Responds to "Leo" wake word and listens for commands  
- 🧠 Chat with AI – Interacts using OpenAI’s GPT model  
- 🌐 Web Automation – Opens popular websites like YouTube, Google, Facebook  
- 🎵 Play Music – Plays songs from a predefined music library via YouTube  
- 🌦️ Weather Forecast – Gives real-time weather updates  
- 📰 News Headlines – Reads the latest tech news  
- 🔋 System Status – Tells current battery level and time  
- 😂 Jokes – Shares programming and tech jokes  
- 🗣️ Text-to-Speech – Speaks responses aloud using `gTTS` or `pyttsx3`  
- 🧠 Context Memory – Maintains conversational context

🛠️ Technologies Used

- Python 3
- OpenAI API (GPT-3.5 Turbo)
- SpeechRecognition
- gTTS / pyttsx3
- Pygame
- Webbrowser, Requests, OS
- NewsAPI & OpenWeatherMap
- dotenv(to manage API keys)

📁 Project Structure
Leo/
├── main.py # Main assistant code
├── musicLibrary.py # Dictionary of songs and YouTube links
├── .env # Environment variables (API keys)
├── README.md # Project documentation
└── requirements.txt # List of dependencies

⚙️ Installation & Setup
1. Clone the repository:

git clone https://github.com/your-username/leo-virtual-assistant.git
cd leo-virtual-assistant

2. Install dependencies:

pip install -r requirements.txt

3.  Create a .env file and add your API keys:

OPENAI_API_KEY=your_openai_api_key
NEWS_API_KEY=your_newsapi_key
WEATHER_API_KEY=your_openweathermap_key

4.  Run the assistant:

python main.py

🧪 Sample Commands

| 🔊 Command                   | 🛠️ Action                              |
| ---------------------------- | --------------------------------------- |
| "Leo" → "Open YouTube"       | Launches YouTube in default browser     |
| "Leo" → "Play Shape of You"  | Plays song from musicLibrary on YouTube |
| "Leo" → "What's the time"    | Speaks current time and battery level   |
| "Leo" → "What's the weather" | Provides current weather conditions     |
| "Leo" → "Tell me a joke"     | Speaks a random tech joke               |
| "Leo" → "What's the news"    | Reads top 5 news headlines              |
| "Leo" → "What is Python?"    | Uses GPT to answer                      |

🧾 .env File Sample

# Rename this to .env and replace with your actual keys
OPENAI_API_KEY=your_openai_api_key
NEWS_API_KEY=your_newsapi_key
WEATHER_API_KEY=your_openweathermap_key

📌 Future Enhancements
- GUI interface using Tkinter or PyQt
- Wake word detection using Snowboy or Vosk
- Support for reminders, timers, and alarms
- Multi-user voice support
- Integration with smart home devices

👤 Author

Avirup Das
CSE Student | Software Developer | Data Analysis Enthusiast
[GitHub](https://github.com/your-username) | [LinkedIn](https://linkedin.com/in/your-link)

📄 License

This project is licensed under the MIT License – feel free to use and modify.
