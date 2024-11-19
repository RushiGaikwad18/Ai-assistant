import speech_recognition as sr

def listen_and_save_to_file():
    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Use microphone as the source
    with sr.Microphone() as source:
        print("Adjusting for ambient noise, please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Listening... Please speak.")

        try:
            # Capture audio
            audio = recognizer.listen(source)

            # Recognize speech using Google Web Speech API
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            print(f"Recognized Text: {text}")

            # Save recognized text to a file
            with open("recognized_speech.txt", "w") as file:
                file.write(text)
            print("Text has been saved to 'recognized_speech.txt'.")

        except sr.UnknownValueError:
            print("Sorry, I couldn't understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

# Call the function
if __name__ == "__main__":
    listen_and_save_to_file()
