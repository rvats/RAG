import speech_recognition as sr
import openai
import constants
import pyttsx3

# Initialize OpenAI API
openai.api_key = constants.APIKEY
tts_engine = pyttsx3.init()
ASSISTANT_NAME = "Arpita Vats"
TRIGGER_PHRASE = "Okay Arpita"
WELCOME_MSG = "Hello Rahul, Welcome Good to See You. How can I help you?"
GOODBYE_MSG = "See you next time."
conversation = [{"role": "system", "assistantName": "Arpita Vats", "content": "DIRECTIVE_FOR_gpt-4o"}]
message = {"role":"user", "content": ""}

def voice_to_text():
    # Initialize the recognizer
    recognizer = sr.Recognizer()
    
    # Use the microphone as the source for input
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        
        # Capture the audio from the microphone
        audio = recognizer.listen(source)
        
    try:
        # Recognize the speech using Google Web Speech API
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"Text: {text}")
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def speak(text):
    print(f"{ASSISTANT_NAME}: {text}")
    tts_engine.say(text)
    tts_engine.runAndWait()

def generate_response(prompt):
    message["content"]=prompt
    conversation.append(message)
    completion = openai.ChatCompletion.create(model="gpt-4o", messages=conversation)
    return completion.choices[0].message.content

if __name__ == "__main__":
    print("Initiating My Personal Assistant: {ASSISTANT_NAME}")
    print("{ASSISTANT_NAME}: {WELCOME_MSG}")
    while True:
        result = voice_to_text()
        if result and result.lower().startswith(TRIGGER_PHRASE.lower()):
            print(f"Converted Text: {result}")
            ai_response = generate_response(result)
            speak(ai_response)
        elif result and result.lower() == "exit":
                print("{ASSISTANT_NAME}: {GOODBYE_MSG}")
                break
        else:
            print("No text could be converted")
