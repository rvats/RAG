import speech_recognition as sr
import openai
import constants
import pyttsx3

# Initialize OpenAI API
openai.api_key = constants.APIKEY
tts_engine = pyttsx3.init()
conversation = [{"role": "system", "content": "DIRECTIVE_FOR_gpt-4o"}]
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
    print(f"Assistant: {text}")
    tts_engine.say(text)
    tts_engine.runAndWait()

def generate_response(prompt):
    message["content"]=prompt
    conversation.append(message)
    completion = openai.ChatCompletion.create(model="gpt-4o", messages=conversation)
    return completion.choices[0].message.content

if __name__ == "__main__":
    print("Please speak something...")
    while True:
        result = voice_to_text()
        if result:
            if result == "exit":
                break
            print(f"Converted Text: {result}")
            ai_response = generate_response(result)
            speak(ai_response)
        else:
            print("No text could be converted")
