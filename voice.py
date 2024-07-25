from sentence_transformers import SentenceTransformer, util
import faiss
import os
import speech_recognition as sr
import openai
import constants
import pyttsx3

# Initialize OpenAI API
openai.api_key = constants.APIKEY
tts_engine = pyttsx3.init()
ASSISTANT_NAME = "RAVE"
TRIGGER_PHRASE = "Okay RAVE"
WELCOME_MSG = "Hello Rahul, Welcome, It's good to See You. How can I help you?"
GOODBYE_MSG = "Goodbye Rahul, See you next time."
doc_folder = 'data'
conversation = [{"role": "system", "assistantName": "RAVE", "content": "DIRECTIVE_FOR_gpt-4o"}]
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
        print("RAVE: Speech Recognition Engine could not understand the audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Speech Recognition Engine; {e}")
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


# prompt = "When is my next dentist appointment?"
# response = process_prompt(prompt, doc_folder)
# print(response)

if __name__ == "__main__":
    print(f"Initiating My Personal Assistant: {ASSISTANT_NAME}")
    speak(WELCOME_MSG)
    while True:
        query = voice_to_text()
        if query and query.lower().startswith(TRIGGER_PHRASE.lower()):
            print(f"Converted Text: {query}")
            response = process_prompt(query, doc_folder)
            ai_response = generate_response(query)
            speak(response)
            # speak(ai_response)
        elif query and query.lower() == "exit":
                speak(GOODBYE_MSG)
                break
        else:
            print(f"{ASSISTANT_NAME}: No text could be converted")
