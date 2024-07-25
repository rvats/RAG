import openai
import constants
import pyttsx3

openai.api_key = constants.APIKEY 

message = {"role":"user", "content": input("This is the beginning of your chat with AI. [To exit, send \"###\".]\n\nYou: ")};
conversation = [{"role": "system", "content": "DIRECTIVE_FOR_gpt-4o"}]
engine = pyttsx3.init()

while(message["content"]!="###"):
    conversation.append(message)
    completion = openai.ChatCompletion.create(model="gpt-4o", messages=conversation) 
    print(f"TWI: {completion.choices[0].message.content}")
    engine.say(completion.choices[0].message.content)
    engine.runAndWait()
    message["content"] = input("You: ")
    conversation.append(completion.choices[0].message)