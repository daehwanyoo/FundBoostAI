from openai import OpenAI

import time

# OpenAI API key


def read_latest_speech():
    """Reads the latest line from the speech_to_text.txt file."""
    try:
        with open("speech_to_text.txt", "r") as f:
            lines = f.readlines()
        if lines:
            latest_text = lines[-1].strip()  # Get the latest line
            return latest_text
        return None
    except FileNotFoundError:
        print("The speech_to_text.txt file was not found.")
        return None

def analyze_text_with_openai(text):
    """Analyze the user's latest response using OpenAI (using the new function-based API)."""
    response = client.completions.create(model="gpt-3.5-turbo-instruct",  # Use the latest available model
    prompt=f"The following is the latest transcript from me(caller) and donor response:\n'{text}'.\nEvaluate my words (caller) is appropriate or not. Respond with one word: 'Appropriate' or 'Inappropriate' and give me a sentence to improve for next one. Also, suggest the top 3 sentences that can be used to elicit a donation based on this context.",
    max_tokens=150)
    result = response.choices[0].text.strip()
    return result

if __name__ == "__main__":
    while True:
        latest_text = read_latest_speech()
        if latest_text:
            print(f"Latest user input: {latest_text}")
            result = analyze_text_with_openai(latest_text)
            print(f"OpenAI evaluation:\n{result}")
        else:
            print("No new input found.")

        time.sleep(5)  # Check for new input every 5 seconds
