import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import time
import urllib.parse
import wikipedia
import openai

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)  # Volume level

# Flag to check if Bro is active or not
is_active = False

# Set up OpenAI API (replace with your actual API key)
openai.api_key = 'your-openai-api-key-here'

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech and return command
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for commands...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)
    
    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio).lower()
        print(f"Command received: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        print("Could not request results, check your network connection.")
        return None

# Function to search Google for a query
def search_google(query):
    """Opens Google search for the given query."""
    search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
    webbrowser.open(search_url)
    speak(f"Here are the Google search results for {query}.")

# Function to search Wikipedia for a person
def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        speak(f"According to Wikipedia: {result}")
    except wikipedia.exceptions.DisambiguationError as e:
        speak(f"There are multiple results for {query}. Please be more specific.")
    except wikipedia.exceptions.PageError:
        speak(f"Sorry, I couldn't find any information about {query} on Wikipedia.")

# Function to ask ChatGPT
def ask_chatgpt(query):
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=query,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

# Function to perform tasks based on command
def perform_task(command):
    global is_active

    print(f"Command: {command}")  # Debugging to see the full command

    # Handling "search" commands
    if 'search' in command:
        query = command.replace('search', '').strip()
        if query:
            speak(f"Searching for {query} on Google...")
            search_google(query)
        else:
            speak("Sorry, I didn't hear the search query.")

    elif 'who is' in command:
        person = command.replace('who is', '').strip()
        if person:
            speak(f"Searching for information about {person} on Wikipedia...")
            search_wikipedia(person)
        else:
            speak("Sorry, I didn't hear the person's name.")

    elif 'ask' in command:
        question = command.replace('ask', '').strip()
        if question:
            speak("Let me think about that...")
            answer = ask_chatgpt(question)
            speak(answer)
        else:
            speak("Sorry, I didn't hear your question.")

    elif 'open google' in command:
        speak("Opening Google...")
        webbrowser.open("http://www.google.com")
    
    elif 'play music' in command:
        speak("Playing music...")
        os.system("start wmplayer")  # Or any media player you want to open
    
    elif 'time' in command:
        current_time = time.strftime("%H:%M:%S")
        speak(f"The current time is {current_time}")
    
    elif 'open notepad' in command:
        speak("Opening Notepad...")
        os.system("notepad")
    
    elif 'calculate' in command:
        speak("What calculation would you like to perform?")
        calculation = recognize_speech()
        if calculation:
            try:
                result = eval(calculation)
                speak(f"The result is {result}")
            except:
                speak("Sorry, I couldn't compute that.")
    
    elif 'shutdown' in command:
        speak("Shutting down the system...")
        os.system("shutdown /s /t 1")  # Shutdown the system
    
    elif 'ok bro' in command and not is_active:
        speak("Bro is now activated.")
        is_active = True
    
    elif 'exit bro' in command and is_active:
        speak("Bro is now deactivated.")
        is_active = False

    else:
        speak("Sorry, I don't know how to perform that task.")

# Main loop
while True:
    command = recognize_speech()
    if command:
        if 'ok bro' in command and not is_active:
            speak("Bro is now activated.")
            is_active = True
        elif 'exit bro' in command and is_active:
            speak("Bro is now deactivated.")
            is_active = False
        elif is_active:
            perform_task(command)