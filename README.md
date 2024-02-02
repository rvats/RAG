# Langchain RAG Tutorial

Install dependencies.

```python
pip install -r requirements.txt
```

Create the Chroma DB.

```python
python create_database.py
```

Query the Chroma DB.

```python
python query_data.py "How does Alice meet the Mad Hatter?"
```

You'll also need to set up an OpenAI account (and set the OpenAI key in your environment variable) for this to work.

# Retrieval Augmented Generation (RAG) for chatbots
RAG enabled Chatbots using [LangChain](https://www.langchain.com) and [Databutton](https://databutton.com/login?utm_source=github&utm_medium=avra&utm_article=rag)
![](https://github.com/avrabyt/RAG-Chatbot/blob/main/thumbnail.webp)

- For the front-end : `app.py`
- PDF parsing and indexing : `brain.py`
- API keys are maintained over databutton secret management
- Indexed are stored over session state 

Oversimplified explanation : (**Retrieval**) Fetch the top N similar contexts via similarity search from the indexed PDF files -> concatanate those to the prompt (**Prompt Augumentation**) -> Pass it to the LLM -> which further generates response (**Generation**) like any LLM does. **More in the blog!**

**Blog Post - [Here](https://medium.com/databutton/why-your-next-ai-product-needs-rag-implemented-in-it-9ee22f9770c8)**

**YouTube video - [Here](https://youtu.be/Yh1GEWqgkt0)**

To get started quickly, you can use the “Chat with PDF” [template](https://databutton.com/new?templateId=pt-x2Rh7dEYwIuCxXaR) within Databutton 🚀

> Alternatively, you can use [Streamlit](https://streamlit.io) to build and deploy! In that case few changes such as `st.secrets` needs to be implemented!

# Similar projects

#### [Building a Simple Chatbot using ChatGPTAPI & Databutton with memory 🧠](https://github.com/avrabyt/MemoryBot)

>Memory implementation can also be an interesting feature in this current RAG enabled Chatbot.

Repo - [MemoryBot](https://github.com/avrabyt/MemoryBot)

The live demo app is hosted over [here](https://next.databutton.com/v/lgzxq112/Memory_Bot)

Blog - [here](https://medium.com/@avra42/how-to-build-a-chatbot-with-chatgpt-api-and-a-conversational-memory-in-python-8d856cda4542) 

Video - [here](https://youtu.be/cHjlperESbg)

#### [PDF Chatbot with Memory](https://github.com/avrabyt/PersonalMemoryBot)
> Similar to Chat with PDF approach, with enabled memory. 

Demo App - [here](https://next.databutton.com/v/lgzxq112/Personalised_Memory_Bot)

Video - [here](https://youtu.be/daMNGGPJkEE)

Blog - [here](https://medium.com/@avra42/how-to-build-a-personalized-pdf-chat-bot-with-conversational-memory-965280c160f8)

![](https://github.com/avrabyt/RAG-Chatbot/blob/main/compare%20medium.gif)

# chatgpt-retrieval

Simple script to use ChatGPT on your own files.

Here's the [YouTube Video](https://youtu.be/9AXP7tCI9PI).

## Installation

Install [Langchain](https://github.com/hwchase17/langchain) and other required packages.
```
pip install langchain openai chromadb tiktoken unstructured
```
Modify `constants.py.default` to use your own [OpenAI API key](https://platform.openai.com/account/api-keys), and rename it to `constants.py`.

Place your own data into `data/data.txt`.

## Example usage
Test reading `data/data.txt` file.
```
> python chatgpt.py "what is my dog's name"
Your dog's name is Sunny.
```

Test reading `data/cat.pdf` file.
```
> python chatgpt.py "what is my cat's name"
Your cat's name is Muffy.

# MultiPDF Chat App

> You can find the tutorial for this project on [YouTube](https://youtu.be/dXxQ0LR-3Hg).

## Introduction
------------
The MultiPDF Chat App is a Python application that allows you to chat with multiple PDF documents. You can ask questions about the PDFs using natural language, and the application will provide relevant responses based on the content of the documents. This app utilizes a language model to generate accurate answers to your queries. Please note that the app will only respond to questions related to the loaded PDFs.

## How It Works
------------

![MultiPDF Chat App Diagram](./docs/PDF-LangChain.jpg)

The application follows these steps to provide responses to your questions:

1. PDF Loading: The app reads multiple PDF documents and extracts their text content.

2. Text Chunking: The extracted text is divided into smaller chunks that can be processed effectively.

3. Language Model: The application utilizes a language model to generate vector representations (embeddings) of the text chunks.

4. Similarity Matching: When you ask a question, the app compares it with the text chunks and identifies the most semantically similar ones.

5. Response Generation: The selected chunks are passed to the language model, which generates a response based on the relevant content of the PDFs.

## Dependencies and Installation
----------------------------
To install the MultiPDF Chat App, please follow these steps:

1. Clone the repository to your local machine.

2. Install the required dependencies by running the following command:
   ```
   pip install -r requirements.txt
   ```

3. Obtain an API key from OpenAI and add it to the `.env` file in the project directory.
```commandline
OPENAI_API_KEY=your_secrit_api_key
```

## Usage
-----
To use the MultiPDF Chat App, follow these steps:

1. Ensure that you have installed the required dependencies and added the OpenAI API key to the `.env` file.

2. Run the `main.py` file using the Streamlit CLI. Execute the following command:
   ```
   streamlit run app.py
   ```

3. The application will launch in your default web browser, displaying the user interface.

4. Load multiple PDF documents into the app by following the provided instructions.

5. Ask questions in natural language about the loaded PDFs using the chat interface.

## Contributing
------------
This repository is intended for educational purposes and does not accept further contributions. It serves as supporting material for a YouTube tutorial that demonstrates how to build this project. Feel free to utilize and enhance the app based on your own requirements.

## License
-------
The MultiPDF Chat App is released under the [MIT License](https://opensource.org/licenses/MIT).