import sounddevice as sd
import numpy as np
import speech_recognition as sr
import time
import threading

# Initialize recognizer
recognizer = sr.Recognizer()

# Duration for checking audio silence
LISTEN_DURATION = 5  # seconds

# Threshold for detecting sound in the computer audio (adjust based on your environment)
COMPUTER_AUDIO_THRESHOLD = 0.02

# Initialize global flags for both audio sources
detected_computer_audio = False
detected_microphone_audio = False

def check_computer_audio(device_index):
    """Captures audio from the system's internal virtual audio stream and prints the detected audio levels."""
    global detected_computer_audio

    def callback(indata, frames, time, status):
        volume_norm = np.linalg.norm(indata) * 10  # normalize audio input
        print(f"[DEBUG] Computer audio volume: {volume_norm}")  # print audio level
        if volume_norm > COMPUTER_AUDIO_THRESHOLD:
            detected_computer_audio = True

    try:
        with sd.InputStream(device=device_index, channels=1, callback=callback):
            sd.sleep(1000)  # Capture for 1 second
    except Exception as e:
        print(f"[ERROR] Failed to capture computer audio: {e}")

def microphone_speech_to_text(mic_device_index):
    """Handles capturing and recognizing audio from the microphone."""
    global detected_microphone_audio
    with sr.Microphone(device_index=mic_device_index) as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Microphone is ready, start speaking...")

        while True:
            print("[DEBUG] Listening for microphone audio...")
            try:
                audio = recognizer.listen(source, timeout=LISTEN_DURATION)
                detected_microphone_audio = True

                # Recognize speech from the microphone
                text = recognizer.recognize_google(audio)
                print(f"Sound in Device (microphone): {text}")

            except sr.UnknownValueError:
                print("Could not understand the audio from microphone.")
            except sr.RequestError as e:
                print(f"Could not request results from microphone; {e}")
            except sr.WaitTimeoutError:
                print("No sound detected from the microphone.")

def computer_audio_to_text(internal_audio_device_index):
    """Handles recognizing audio from the internal computer audio (virtual device)."""
    global detected_computer_audio

    while True:
        print("[DEBUG] Listening for computer audio...")
        check_computer_audio(internal_audio_device_index)
        if detected_computer_audio:
            print("[DEBUG] Sound in computer detected. Processing...")
            print("Sound in computer: <Transcribed internal audio content>")
            detected_computer_audio = False  # Reset after detection

def main(mic_device_index, internal_audio_device_index):
    # Create threads for microphone and internal audio processing
    mic_thread = threading.Thread(target=microphone_speech_to_text, args=(mic_device_index,))
    computer_audio_thread = threading.Thread(target=computer_audio_to_text, args=(internal_audio_device_index,))

    # Start both threads
    mic_thread.start()
    computer_audio_thread.start()

    # Join the threads (wait for them to complete)
    mic_thread.join()
    computer_audio_thread.join()

if __name__ == "__main__":
    # Get the indices for microphone and virtual audio device (system audio)
    mic_device_index = None  # None defaults to the system microphone
    internal_audio_device_index = 1  # Replace with the correct index for your virtual device

    # Check available devices
    print("Available audio devices:")
    print(sd.query_devices())

    main(mic_device_index, internal_audio_device_index)
