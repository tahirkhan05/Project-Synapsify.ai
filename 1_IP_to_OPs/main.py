import os
from dotenv import load_dotenv

load_dotenv()

gemini_audience = input("Gemini audience: ")
gpt_audience = input("GPT audience: ")
groq_audience = input("Groq audience: ")

question = input("You: ")

from gemini_chatbot import get_gemini_response
from gpt_chatbot import get_gpt_response
from groq_chatbot import get_groq_response

gemini_response = get_gemini_response(gemini_audience, question)
gpt_response = get_gpt_response(gpt_audience, question)
groq_response = get_groq_response(groq_audience, question)

print("Gemini response:")
print(gemini_response)
print("GPT response:")
print(gpt_response)
print("Groq response:")
print(groq_response)