import speech_recognition as sr
import openai
import os

openai.api_key = os.getenv("API KEY")

completion=openai.Completion()

def Reply(donor):
    response=completion.create(
        model="gpt-3.5-turbo",
         messages=[
        {"role": "system", "content": "You are a helpful assistant to create a script to ultimately persuading potential donors. Bring me one or two or even three sentences to respond or a question for what donor said"},
        {"role": "user", "content": "{donor}"},
    ]
)
    answer=response.choices[0].message
    return answer

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
            print(words)

        except Exception as e:
            print("Couldn't recognize what you said, speak once more.")

if __name__ == '__main__':
    while True:
        query=recognize_speech().lower()
        ans=Reply(query)
        print(ans)
        if 'bye' in query:
            break

        if "stop" in query:
            print("Stop word detected. Exiting...")
            break
