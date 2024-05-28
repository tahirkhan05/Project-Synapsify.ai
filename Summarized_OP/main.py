import os
from dotenv import load_dotenv
import time
import sys
import logging
from transformers import BartTokenizer, BartForConditionalGeneration

load_dotenv()

from gemini_chatbot import get_gemini_response
from gpt_chatbot import get_gpt_response
from groq_chatbot import get_groq_response

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
last_selected_chatbot = None

# Load BART model and tokenizer for summarization
tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

# Set default language to English
language = 'English'

# Option to change language
user_language = input("Select Language (or press Enter to use default 'English'): ").strip()
if user_language:
    language = user_language

while len(selected_chatbots) < max_selections:
    print("Select a chatbot (or 'done' to finish selecting):")
    print("1. gemini")
    print("2. gpt")
    print("3. groq")
    choice = input("Your choice (or press Enter to reuse the last selected chatbot): ")

    if choice == 'done':
        break

    if choice == '' and last_selected_chatbot:
        chatbot = last_selected_chatbot
    elif choice in ['1', '2', '3']:
        chatbot = ['gemini', 'gpt', 'groq'][int(choice) - 1]
        last_selected_chatbot = chatbot
    else:
        print("Invalid choice. Please select again.")
        continue

    instance_number = len(selected_chatbots) + 1
    api_key_var = chatbot_keys[chatbot] + str(instance_number)
    api_key = os.getenv(api_key_var)

    if api_key is None:
        logging.error(f"API key for {chatbot} instance {instance_number} not found. Check your .env file.")
        continue

    audience = input(f"{chatbot.capitalize()} audience (or press Enter for default '{default_audience}'): ").strip()
    if not audience:
        audience = default_audience
    selected_chatbots.append((chatbot, api_key, audience, []))  # Adding an empty list for chat history

# Ask the user if they want summarized output
summarize_output = input("Would you like a summarized output of chatbot responses? (yes/no): ").strip().lower()
if summarize_output not in ['yes', 'no']:
    print("Invalid choice. Defaulting to 'no'.")
    summarize_output = 'no'

while True:
    question = input("You: ")
    if question.lower() == 'exit':
        break

    responses = []

    for i, (chatbot, api_key, audience, history) in enumerate(selected_chatbots):
        try:
            response, updated_history = chatbot_functions[chatbot](audience, language, question, api_key, history)
            selected_chatbots[i] = (chatbot, api_key, audience, updated_history)
            responses.append((chatbot, audience, response))
        except Exception as e:
            logging.error(f"Error getting response from {chatbot}: {e}")
            responses.append((chatbot, audience, "An error occurred while fetching the response. Please try again later."))

    for chatbot, audience, response in responses:
        print(f"{chatbot.capitalize()} response for audience '{audience}':")
        for char in response:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.01)  # adjust the delay as needed
        print("\n")

    if summarize_output == 'yes':
        combined_responses = " ".join([f"{chatbot} said: {response}" for chatbot, audience, response in responses])
        inputs = tokenizer.encode(combined_responses, return_tensors='pt', max_length=1024, truncation=True)
        summary_ids = model.generate(inputs, max_length=1000, min_length=200, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        print("Summary of responses:")
        for char in summary:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.01)  # adjust the delay as needed
        print("\n")
