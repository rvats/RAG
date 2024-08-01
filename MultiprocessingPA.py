from sentence_transformers import SentenceTransformer, util
import faiss
import os
import speech_recognition as sr
import openai
import constants
import pyttsx3
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
import threading
import logging

# Initialize colorama and logging
colorama_init()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize OpenAI API
openai.api_key = constants.APIKEY
tts_engine = pyttsx3.init()
tts_lock = threading.Lock()  # Lock to manage access to TTS engine
ASSISTANT_NAME = "RAVE"
TRIGGER_PHRASES = ["OKAY RAVE", "TADA", "OKAY E Y", "OKAY EBAY", "OKAY BYE", "OKAY ELI", "OKAY IF I", "OK E Y", "OK RAVE"]
WELCOME_MSG = "Hello Rahul, Welcome, It's good to See You. How can I help you?"
GOODBYE_MSG = "Goodbye Rahul, See you next time."
doc_folder = 'data'
conversation = [{"role": "system", "assistantName": "RAVE", "assistantName": "E Y", "assistantName": "TADA", "content": "DIRECTIVE_FOR_gpt-4o"}]
message = {"role":"user", "content": ""}

def voice_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        logging.info("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        logging.info("Listening...")
        audio = recognizer.listen(source)
    try:
        logging.info("Recognizing...")
        text = recognizer.recognize_google(audio)
        logging.info(f"Text: {text}")
        return text
    except sr.UnknownValueError:
        logging.error(f"{ASSISTANT_NAME}: Speech Recognition Engine could not understand the audio")
        return None
    except sr.RequestError as e:
        logging.error(f"Could not request results from Speech Recognition Engine; {e}")
        return None

def speak(text):
    with tts_lock:
        logging.info(f"{ASSISTANT_NAME}: {text}")
        tts_engine.say(text)
        tts_engine.runAndWait()

def generate_response(prompt):
    message["content"] = prompt
    conversation.append(message)
    try:
        completion = openai.ChatCompletion.create(model="gpt-4o", messages=conversation)
        return completion.choices[0].message.content
    except Exception as e:
        logging.error(f"Error generating response from OpenAI: {e}")
        return "I'm sorry, I couldn't process your request."

model = SentenceTransformer('all-MiniLM-L6-v2')

def load_documents(doc_folder):
    documents = []
    for filename in os.listdir(doc_folder):
        if filename.endswith(".txt"):
            with open(os.path.join(doc_folder, filename), 'r', encoding='utf-8') as file:
                documents.append(file.read())
    return documents

def create_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

def retrieve_documents(query, index, embeddings, documents, top_k=5):
    query_embedding = model.encode(query, convert_to_tensor=True)
    scores, indices = index.search(query_embedding.unsqueeze(0).cpu().numpy(), top_k)
    return [documents[idx] for idx in indices[0]]

def generate_response_with_context(prompt, context):
    full_prompt = f"Context:\n{context}\n\nQuestion: {prompt}\n\nAnswer:"
    return generate_response(full_prompt)

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

def listen_and_process():
    while True:
        query = voice_to_text()
        if query:
            triggerFound = starts_with_trigger(query)
            if triggerFound:
                query = update_trigger_phrase(query)
                logging.info(f"Converted Text: {query}")
                response = process_prompt(query, doc_folder)
                threading.Thread(target=speak, args=(response,)).start()
            elif query.lower() == "exit":
                speak(GOODBYE_MSG)
                break
        else:
            logging.info(f"{ASSISTANT_NAME}: No text could be converted")

if __name__ == "__main__":
    logging.info(f"Initiating My Personal Assistant: {ASSISTANT_NAME}")
    speak(WELCOME_MSG)
    
    listen_thread = threading.Thread(target=listen_and_process)
    listen_thread.start()
    listen_thread.join()
