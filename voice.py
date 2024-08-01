from sentence_transformers import SentenceTransformer, util
import faiss
import os
import speech_recognition as sr
import openai
import constants
import pyttsx3
import json
import keyboard
import multiprocessing
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

colorama_init()
# Load configuration from JSON
def load_config(config_file):
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config

config = load_config('config.json')
# Initialize OpenAI API
openai.api_key = constants.APIKEY

ASSISTANT_NAME = config["ASSISTANT_NAME"]
TRIGGER_PHRASES = config["TRIGGER_PHRASES"]
EXIT_PHRASES = config["EXIT_PHRASES"]
WELCOME_MSG = config["WELCOME_MSG"]
GOODBYE_MSG = config["GOODBYE_MSG"]
doc_folder = config["doc_folder"]
conversation = config["conversation"]
message = config["message"]

def voice_to_text():
    # Initialize the recognizer
    recognizer = sr.Recognizer()
    
    # Use the microphone as the source for input
    with sr.Microphone() as source:
        print(f"{Fore.YELLOW}{Style.DIM}Adjusting for ambient noise...{Style.RESET_ALL}")
        recognizer.adjust_for_ambient_noise(source)
        print(f"{Fore.YELLOW}{Style.DIM}Listening...{Style.RESET_ALL}")
        
        # Capture the audio from the microphone
        audio = recognizer.listen(source)
        
    try:
        # Recognize the speech using Google Web Speech API
        print(f"{Fore.YELLOW}{Style.DIM}Recognizing...{Style.RESET_ALL}")
        text = recognizer.recognize_google(audio)
        print(f"{Fore.GREEN}{Style.BRIGHT}Text: {text}{Style.RESET_ALL}")
        return text
    except sr.UnknownValueError:
        print(f"{Fore.RED}{Style.BRIGHT}{ASSISTANT_NAME}: Speech Recognition Engine could not understand the audio{Style.RESET_ALL}")
        return None
    except sr.RequestError as e:
        print(f"{Fore.RED}{Style.BRIGHT}Could not request results from Speech Recognition Engine; {e}{Style.RESET_ALL}")
        return None

def sayFunc(phrase):
    engine = pyttsx3.init()
    engine.setProperty('voice', r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
    engine.say(phrase)
    engine.runAndWait()

def say(phrase):
	if __name__ == "__main__":
		p = multiprocessing.Process(target=sayFunc, args=(phrase,))
		p.start()
		while p.is_alive():
			if keyboard.is_pressed('q') or keyboard.is_pressed('esc'):
				p.terminate()
			else:
				continue
		p.join()

def speak(text):
    print(f"{Fore.CYAN}{Style.BRIGHT}{ASSISTANT_NAME}: {Fore.LIGHTWHITE_EX}{Style.NORMAL}{text}{Style.RESET_ALL}")
    say(text)


def generate_response(prompt):
    message["content"]=prompt
    conversation.append(message)
    completion = openai.ChatCompletion.create(model="gpt-4o", messages=conversation)
    return completion.choices[0].message.content

model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to load documents
def load_documents(doc_folder):
    documents = []
    for filename in os.listdir(doc_folder):
        if filename.endswith(".txt"):
            with open(os.path.join(doc_folder, filename), 'r', encoding='utf-8') as file:
                documents.append(file.read())
    return documents

# Function to create FAISS index
def create_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

# Function to retrieve relevant documents
def retrieve_documents(query, index, embeddings, documents, top_k=5):
    query_embedding = model.encode(query, convert_to_tensor=True)
    scores, indices = index.search(query_embedding.unsqueeze(0).cpu().numpy(), top_k)
    return [documents[idx] for idx in indices[0]]

# Function to generate response using GPT-4
def generate_response_with_context(prompt, context):
    full_prompt = f"Context:\n{context}\n\nQuestion: {prompt}\n\nAnswer:"
    return generate_response(full_prompt)

# Main function to handle prompt
def process_prompt(prompt, doc_folder):
    documents = load_documents(doc_folder)
    embeddings = model.encode(documents, convert_to_tensor=True)
    faiss_index = create_faiss_index(embeddings.cpu().numpy())
    relevant_docs = retrieve_documents(prompt, faiss_index, embeddings, documents)
    context = "\n\n".join(relevant_docs)
    response = generate_response_with_context(prompt, context)
    return response


def starts_with_trigger(query):
    if query:
        query_upper = query.upper()
        for phrase in TRIGGER_PHRASES:
            if query_upper.startswith(phrase):
                return True
    return False

def update_trigger_phrase(query):
    if query:
        query_upper = query.upper()
        for phrase in TRIGGER_PHRASES:
            if query_upper.startswith(phrase):
                query = 'Okay RAVE ' + query[len(phrase):].lstrip()
    return query

if __name__ == "__main__":
    print(f"{Fore.GREEN}{Style.BRIGHT}Initiating My Personal Assistant: {Fore.CYAN}{Style.BRIGHT}{ASSISTANT_NAME}{Style.RESET_ALL}")
    speak(WELCOME_MSG)
    while True:
        query = voice_to_text()
        triggerFound = starts_with_trigger(query)
        if query and triggerFound:
            query = update_trigger_phrase(query)
            print(f"{Fore.YELLOW}{Style.BRIGHT}Converted Text: {query}{Style.RESET_ALL}")
            response = process_prompt(query, doc_folder)
            ai_response = generate_response(query)
            speak(response)
            # speak(ai_response)
        elif query and query.upper() in EXIT_PHRASES:
                speak(GOODBYE_MSG)
                break
        else:
            print(f"{Fore.LIGHTWHITE_EX}{Style.DIM}{ASSISTANT_NAME}: No text could be converted{Style.RESET_ALL}")
