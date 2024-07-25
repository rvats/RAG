import speech_recognition as sr
import pyttsx3
import openai
import constants
from flask import Flask, request, jsonify

# Initialize OpenAI API
openai.api_key = constants.APIKEY

# Initialize Speech Recognition and Text-to-Speech
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()
conversation = [{"role": "system", "content": "DIRECTIVE_FOR_gpt-4o"}]
message = {"role":"user", "content": ""}
app = Flask(__name__)

def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        # Capture the audio from the microphone
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio)
        print(f"User said: {query}")
        return query
    except Exception as e:
        print("Could not understand audio")
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

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('input', 'Hello')
    
    if user_input:
        ai_response = generate_response(user_input)
        speak(ai_response)
        return jsonify({'response': ai_response})
    else:
        return jsonify({'response': 'Invalid input'}), 400

if __name__ == '__main__':
    # Start the Flask web server
    app.run(debug=True)

    # For command-line interaction
    while True:
        user_query = listen()
        if user_query:
            response = generate_response(user_query)
            speak(response)
