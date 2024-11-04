import speech_recognition as sr
import pyaudio
from openai import OpenAI

client = OpenAI(api_key="")
import os
import keyboard
import sounddevice as sd


messages=[]
evluation=[]

def potentialQ(amount, edu, loca):
    response = client.chat.completions.create(model="text-davinci-003",
    prompt=f"The alunmi donated {amount}, finished his/her {edu} degree and now he/she is living in {loca}. Based on those information bring three questions to ask to the alumni to become close each other and eventually make comfortable to ask donation to campus",
    max_tokens=7,
    temperature=0)
    answer = response.choices[0].text.strip()
    print(answer)


def evaluate(donor):
    response = client.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Your goal is to evaluate/analyze the latest user's response or question to the donor. Give me one word whether it was appropriate or not and a single sentence of what can it be improved."},
        {"role": "user", "content": f"{donor}"},
    ])
    answer = response.choices[0].message.content.strip()
    return answer


def recognize_donor(device_index):
    r = sr.Recognizer()
    mic = sr.Microphone(device_index)

    while True:
        with mic as source:
            r.pause_threshold = 1
            print("Listening...")
            audio = r.listen(source)
            r.adjust_for_ambient_noise(source)
        try:
            query = r.recognize_google(audio, language='en-in')
            print("Donor: "f"{query}")
            return query
        except Exception as e:
            print("Skip")

def recognize_you(device_index):
    r = sr.Recognizer()
    mic = sr.Microphone(device_index)

    while True:
        with mic as source:
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language='en-in')
            print("You: "f"{query}")
            return query
        except Exception as e:
            print("Skip")

if __name__ == '__main__':
    print(sd.query_devices())

    you_audio_index = int(input("Type the index of your audio('>'): "))
    donor_audio_index = int(input("Type the index of donor's audio('<'): "))
    print("\n\n\n")

    #donor_previous=input("Enter the latest donation amount: ")
    #donor_education=input("Enter the education level: ")
    #donor_location=input("Enter the address of the donor(state and city): ")

    #potentialQ(donor_previous, donor_education, donor_location)

    text=input("Type enter to start evaluating")
    if text=="":
        while True:
            you_query = recognize_you(you_audio_index).lower()
            #messages.append({"role": "user", "content":f"User:{you_query}"})
            #evluation.append("I: f'{you_query}")
            #temp=evaluate(messages)
            #print("Suggestion: f'{temp}\n")
            #evluation.append("Suggestion: f'{temp}")
            donor_query = recognize_donor(donor_audio_index).lower()
            #messages.append({"role": "user", "content":f"Donor:{donor_query}"})
            #evluation.append("Donor: f'{donor_query}")
            if "stop" in you_query:
                break