# assistant.py
import speech_recognition as sr
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
        # Initialize TTS engine; try sapi5 (Windows) and fallback to default
        try:
            self.engine = pyttsx3.init('sapi5')
        except Exception:
            self.engine = pyttsx3.init()
        self.engine.setProperty('rate', VOICE_RATE)
        self.engine.setProperty('volume', VOICE_VOLUME)
        voices = self.engine.getProperty('voices')
        if voices:
            self.engine.setProperty('voice', voices[0].id)

        self.recognizer = sr.Recognizer()
        # Adjust thresholds to reduce background noise
        self.recognizer.energy_threshold = 300
        self.recognizer.pause_threshold = 0.7

    def speak(self, text: str):
        print("NEO:", text)
        self.engine.say(text)
        self.engine.runAndWait()

    def listen_once(self, timeout=6, phrase_time_limit=6) -> str:
        with sr.Microphone() as source:
            # adjust for ambient noise briefly
            self.recognizer.adjust_for_ambient_noise(source, duration=0.6)
            print("Listening...")
            try:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                query = self.recognizer.recognize_google(audio, language='en-in')
                print("Heard:", query)
                return query.lower()
            except sr.WaitTimeoutError:
                print("Listening timeout.")
                return ""
            except Exception as e:
                print("Listen error:", e)
                return ""

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
            self.speak("I didn't catch that. Please try again.")
            return "no-input"

        # Wikipedia
        if 'wikipedia' in query:
            topic = query.replace('wikipedia', '').strip()
            if not topic:
                self.speak("Please say the topic after saying Wikipedia.")
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

        # Send email (simple parsing)
        if 'send email' in query:
            # expects: send email to <email> subject <subject> body <body>
            parts = query.split()
            try:
                if 'to' in parts and 'subject' in parts and 'body' in parts:
                    to_idx = parts.index('to') + 1
                    subj_idx = parts.index('subject') + 1
                    body_idx = parts.index('body') + 1
                    to_address = parts[to_idx]
                    subject = ' '.join(parts[subj_idx:parts.index('body')])
                    body = ' '.join(parts[body_idx:])
                    ok = send_email(to_address, subject, body)
                    if ok:
                        self.speak('Email sent successfully.')
                        return 'email-sent'
                    else:
                        self.speak('Failed to send email.')
                        return 'email-failed'
                else:
                    self.speak('Please say: send email to <email> subject <subject> body <body>')
                    return 'email-incomplete'
            except Exception as e:
                print('Email parse/send error', e)
                return str(e)

        # WhatsApp
        if 'send whatsapp' in query or 'whatsapp' in query:
            # expects: send whatsapp to <phone> message <text>
            parts = query.split()
            try:
                if 'to' in parts and 'message' in parts:
                    to_idx = parts.index('to') + 1
                    msg_idx = parts.index('message') + 1
                    phone = parts[to_idx]
                    message = ' '.join(parts[msg_idx:])
                    send_whatsapp_message(phone, message)
                    self.speak('WhatsApp message scheduled. Browser will open.')
                    return 'whatsapp-scheduled'
                else:
                    self.speak('Please say: send whatsapp to <phone> message <text>')
                    return 'whatsapp-incomplete'
            except Exception as e:
                print('WhatsApp error', e)
                return str(e)

        # Screenshot
        if 'screenshot' in query or 'take screenshot' in query:
            path = take_screenshot()
            self.speak(f'Screenshot saved to {path}')
            return path

        # Fallback
        self.speak('Sorry, I did not understand the command.')
        return 'unknown-command'
