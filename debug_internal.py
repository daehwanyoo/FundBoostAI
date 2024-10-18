import speech_recognition as sr
import pyaudio

# Initialize recognizer
recognizer = sr.Recognizer()

# Function to list available audio devices
def list_audio_devices():
    p = pyaudio.PyAudio()
    device_list = []
    print("Available audio devices:")
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        device_list.append(device_info)
        print(f"{i}: {device_info['name']}")
    return device_list

def microphone_speech_to_text(device_index):
    # Set the microphone based on user's selected device index
    with sr.Microphone(device_index=device_index) as source:
        recognizer.adjust_for_ambient_noise(source)
        print(f"Microphone {device_index} is ready, start speaking...")

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

if __name__ == "__main__":
    # List available audio devices and let user choose
    devices = list_audio_devices()
    selected_device_index = int(input("Enter the index of the audio device you want to use: "))

    # Start speech-to-text with the selected device
    microphone_speech_to_text(selected_device_index)
