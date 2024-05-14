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

while(True):
  question = input("You:  ")

  if(question.strip() == ''):
    break

  response = chat.send_message(question)
  print('\n')
  print(f"Gemini: {response.text}")
  print('\n')
