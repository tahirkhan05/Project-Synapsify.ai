import os
from dotenv import load_dotenv
import time
import sys
import logging
import spacy
import pytextrank
from sentence_transformers import SentenceTransformer, util

# Load SpaCy model and add TextRank to the pipeline
nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('textrank')

# Load Sentence Transformer model
sbert_model = SentenceTransformer('all-MiniLM-L6-v2')

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

def summarize_responses(responses):
    combined_responses = " ".join(response for _, _, response in responses)
    doc = nlp(combined_responses)

    # Extract top sentences using TextRank
    summary_sentences = []
    for sent in doc._.textrank.summary(limit_phrases=15, limit_sentences=15):
        summary_sentences.append(sent.text)

    # Ensure sentences are complete and not truncated
    filtered_sentences = []
    for sent in summary_sentences:
        if sent.endswith('.') or sent.endswith('?') or sent.endswith('!'):
            filtered_sentences.append(sent)
        else:
            # Try to merge with the next sentence if the current one is incomplete
            current_index = summary_sentences.index(sent)
            if current_index + 1 < len(summary_sentences):
                sent += " " + summary_sentences[current_index + 1]
                if sent.endswith('.') or sent.endswith('?') or sent.endswith('!'):
                    filtered_sentences.append(sent)

    # Encode sentences and filter out similar ones
    sentence_embeddings = sbert_model.encode(filtered_sentences)
    unique_sentences = []
    used_indices = set()

    for i, embedding in enumerate(sentence_embeddings):
        if i in used_indices:
            continue
        unique_sentences.append(filtered_sentences[i])
        for j in range(i + 1, len(sentence_embeddings)):
            if j in used_indices:
                continue
            if util.pytorch_cos_sim(embedding, sentence_embeddings[j]) > 0.8:
                used_indices.add(j)

    return " ".join(unique_sentences)

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

    summary = summarize_responses(responses)
    print("Summary of responses:")
    for char in summary:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.01)
    print("\n")