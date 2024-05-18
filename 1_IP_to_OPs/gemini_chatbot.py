import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(
    api_key = API_KEY
)

model = genai.GenerativeModel('gemini-1.5-pro-latest')
chat = model.start_chat(history=[])

def get_gemini_response(audience, question):
    instruction = f"In this chat, respond as if you're explaining things to a {audience}. "
    response = chat.send_message(instruction + question)
    return response.text
