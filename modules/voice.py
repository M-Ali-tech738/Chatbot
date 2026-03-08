import streamlit as st
import speech_recognition as sr
import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return None

def voice_input():
    voice_input_button = st.button("", key="voice_input_button")
    if voice_input_button:
        user_question = listen()
        if user_question:
            st.write("You said:", user_question)
            return user_question
    return None

