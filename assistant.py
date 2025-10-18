# assistant.py (Streamlit Compatible Version)
import pyttsx3
import webbrowser
import wikipedia
import pywhatkit
import os
from config import VOICE_RATE, VOICE_VOLUME
from email_utils import send_email
from whatsapp_utils import send_whatsapp_message
from utils import take_screenshot, current_time_str

class NEOAssistant:
    def __init__(self):
        # Remove speech recognition for Streamlit
        try:
            self.engine = pyttsx3.init()
        except Exception:
            self.engine = None
            
        if self.engine:
            self.engine.setProperty('rate', VOICE_RATE)
            self.engine.setProperty('volume', VOICE_VOLUME)
            voices = self.engine.getProperty('voices')
            if voices:
                self.engine.setProperty('voice', voices[0].id)

    def speak(self, text: str):
        # For Streamlit: print text instead of voice
        print("NEO:", text)

    def greet_by_time(self):
        from datetime import datetime
        hour = datetime.now().hour
        if 12 <= hour < 18:
            self.speak("Good Afternoon Sir. Have you had your lunch?")
        elif 18 <= hour < 24:
            self.speak("Good Evening Sir.")
        else:
            self.speak("Good Morning Sir.")

    def handle_command(self, query: str) -> str:
        if not query:
            self.speak("I didn't catch that. Please type a command.")
            return "no-input"

        # Wikipedia
        if 'wikipedia' in query:
            topic = query.replace('wikipedia', '').strip()
            if not topic:
                self.speak("Please type the topic after saying Wikipedia.")
                return "no-topic"
            try:
                summary = wikipedia.summary(topic, sentences=2)
                self.speak('According to Wikipedia:')
                self.speak(summary)
                return summary
            except Exception as e:
                self.speak('Sorry, could not find that on Wikipedia.')
                return f'error: {e}'

        # Open websites
        if 'open youtube' in query:
            webbrowser.open('https://www.youtube.com')
            self.speak('Opening YouTube')
            return 'opened youtube'
        if 'open google' in query:
            webbrowser.open('https://www.google.com')
            self.speak('Opening Google')
            return 'opened google'
        if 'open github' in query:
            webbrowser.open('https://github.com')
            self.speak('Opening GitHub')
            return 'opened github'
        if 'open linkedin' in query:
            webbrowser.open('https://www.linkedin.com')
            self.speak('Opening LinkedIn')
            return 'opened linkedin'

        # Play music / play song
        if 'play music' in query or 'play song' in query:
            song = query.replace('play music', '').replace('play song', '').strip()
            if not song:
                song = 'lofi hip hop'
            try:
                pywhatkit.playonyt(song)
                self.speak(f'Playing {song} on YouTube')
                return f'playing {song}'
            except Exception as e:
                print("play error", e)
                return f'error: {e}'

        # Time
        if 'time' in query:
            t = current_time_str()
            self.speak('The current time is ' + t)
            return t

        # Send email
        if 'send email' in query:
            return "Email feature available in desktop version only."

        # WhatsApp
        if 'whatsapp' in query:
            return "WhatsApp feature available in desktop version only."

        # Screenshot
        if 'screenshot' in query or 'take screenshot' in query:
            path = take_screenshot()
            self.speak(f'Screenshot saved to {path}')
            return path

        # Fallback
        self.speak('Sorry, I did not understand the command.')
        return 'unknown-command'



