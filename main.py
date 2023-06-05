import speech_recognition as sr

def recognize_speech():
    r = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = r.listen(source)
        try:
            print("Recognizing...")
            query= r.recognize_google(audio,language= 'en-in')
            words = query.split()
            for word in words:
                print(word)
            if "stop" in words:
                print("Stop word detected. Exiting...")
                break
            with open("recognized.txt", "a") as file:
                file.write(query + "\n")

        except Exception as e:
            print("Miss stark couldn't recognize what you said, speak once more.")

recognize_speech() 