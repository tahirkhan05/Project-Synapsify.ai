import os
from dotenv import load_dotenv
import time
import sys

load_dotenv()

from gemini_chatbot import get_gemini_response
from gpt_chatbot import get_gpt_response
from groq_chatbot import get_groq_response

chatbot_functions = {
    'gemini': get_gemini_response,
    'gpt': get_gpt_response,
    'groq': get_groq_response
}

chatbot_keys = {
    'gemini': 'GEMINI_API_KEY_',
    'gpt': 'OPENAI_API_KEY_',
    'groq': 'LLAMA_API_KEY_'
}

selected_chatbots = []
max_selections = 4
default_audience = 'general public'

while len(selected_chatbots) < max_selections:
    print("Select a chatbot (or 'done' to finish selecting):")
    print("1. gemini")
    print("2. gpt")
    print("3. groq")
    choice = input("Your choice: ")
    
    if choice == 'done':
        break

    if choice in ['1', '2', '3']:
        chatbot = ['gemini', 'gpt', 'groq'][int(choice) - 1]
        instance_number = len(selected_chatbots) + 1
        api_key_var = chatbot_keys[chatbot] + str(instance_number)
        api_key = os.getenv(api_key_var)

        if api_key is None:
            print(f"API key for {chatbot} instance {instance_number} not found. Check your .env file.")
            continue
        
        audience = input(f"{chatbot.capitalize()} audience (or press Enter for default '{default_audience}'): ").strip()
        if not audience:
            audience = default_audience
        selected_chatbots.append((chatbot, api_key, audience, []))  # Adding an empty list for chat history
    else:
        print("Invalid choice. Please select again.")

while True:
    question = input("You: ")
    if question.lower() == 'exit':
        break

    responses = []

    for i, (chatbot, api_key, audience, history) in enumerate(selected_chatbots):
        response, updated_history = chatbot_functions[chatbot](audience, question, api_key, history)
        selected_chatbots[i] = (chatbot, api_key, audience, updated_history)
        responses.append((chatbot, audience, response))

    for chatbot, audience, response in responses:
        print(f"{chatbot.capitalize()} response for audience '{audience}':")
        for char in response:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.02)  # adjust the delay as needed
        print("\n")
