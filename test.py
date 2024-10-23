import pyaudio
import sounddevice as sd
import numpy as np
import speech_recognition as sr
import threading

# Initialize recognizer
recognizer = sr.Recognizer()

# Function to list available audio devices for internal audio (pyaudio)
def list_audio_devices():
    p = pyaudio.PyAudio()
    device_list = []
    print("Available audio devices:")
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        device_list.append(device_info)
        print(f"{i}: {device_info['name']}")
    return device_list

# Function to capture and process microphone audio
def microphone_speech_to_text():
    """Captures audio from microphone and performs speech-to-text"""
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
            except sr.UnknownValueError:
                print("Could not understand the audio from microphone.")
            except sr.RequestError as e:
                print(f"Could not request results from microphone; {e}")
            except sr.WaitTimeoutError:
                print("No sound detected from microphone.")

# Function to capture and process system audio from selected device
def system_audio_speech_to_text(device_index, channels=2):
    """Captures system audio from the selected device and performs speech-to-text"""
    def callback(indata, frames, time, status):
        volume_norm = np.linalg.norm(indata) * 10  # Normalize the audio input
        print(f"[DEBUG] System audio volume: {volume_norm}")
        if volume_norm > 0.01:  # Adjust this threshold if necessary
            print("System audio detected!")
            try:
                audio_data = sr.AudioData(indata.tobytes(), 16000, channels)
                text = recognizer.recognize_google(audio_data)
                print(f"Recognized system audio: {text}")
            except sr.UnknownValueError:
                print("System audio could not be understood.")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech API; {e}")

    try:
        with sd.InputStream(device=device_index, channels=channels, callback=callback):
            print(f"Listening for system audio on device {device_index} (channels={channels})...")
            sd.sleep(10000)  # Capture for 10 seconds
    except Exception as e:
        print(f"[ERROR] Failed to capture system audio: {e}")

def start_audio_capture():
    # Step 1: List available audio devices for system audio capture
    devices = list_audio_devices()

    # Step 2: Ask the user to choose the device index for internal system audio
    selected_device_index = int(input("Enter the index of the audio device you want to use for system audio: "))

    # Step 3: Create threads for both microphone and system audio
    mic_thread = threading.Thread(target=microphone_speech_to_text)
    system_audio_thread = threading.Thread(target=system_audio_speech_to_text, args=(selected_device_index, 2))

    # Step 4: Start both threads
    mic_thread.start()
    system_audio_thread.start()

    # Step 5: Join the threads to make them run simultaneously
    mic_thread.join()
    system_audio_thread.join()

if __name__ == "__main__":
    start_audio_capture()
