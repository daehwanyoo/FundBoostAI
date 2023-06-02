import speech_recognition as sr

def recognize_speech():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)

        while True:
            audio = r.listen(source)

            try:
                text = r.recognize_google(audio)

                words = text.split()
                for word in words:
                    print(word)
                if "stop" in words:
                    print("Stop word detected. Exiting...")
                    break

            except sr.UnknownValueError:
                print("Could not understand audio.")
            except sr.RequestError as e:
                print("Error: {0}".format(e))

recognize_speech()