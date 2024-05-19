import os
from .gemini_chatbot import get_gemini_response
from .gpt_chatbot import get_gpt_response
from .groq_chatbot import get_groq_response

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

def get_response_from_chatbot(chatbot, audience, question):
    instance_number = 1  # Assuming a single instance for simplicity
    api_key_var = chatbot_keys[chatbot] + str(instance_number)
    api_key = os.getenv(api_key_var)
    
    if not api_key:
        return f"API key for {chatbot} instance {instance_number} not found. Check your .env file."
    
    response = chatbot_functions[chatbot](audience, question, api_key)
    return response
