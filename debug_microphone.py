import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

def microphone_speech_to_text():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Microphone is ready, start speaking...")

        while True:
            try:
                print("Listening for microphone audio...")
                audio = recognizer.listen(source, timeout=5)
                # Recognize speech from microphone
                text = recognizer.recognize_google(audio)
                print(f"Microphone detected: {text}")
                # Write the recognized text to file for main.py to process
                with open("speech_to_text.txt", "a") as f:
                    f.write(f"Me (caller): {text}\n")
            except sr.UnknownValueError:
                print("Could not understand the audio from microphone.")
            except sr.RequestError as e:
                print(f"Could not request results from microphone; {e}")
            except sr.WaitTimeoutError:
                print("No sound detected from microphone.")

if __name__ == "__main__":
    microphone_speech_to_text()
