import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(
  api_key=API_KEY
)

history = []

def get_gpt_response(audience, question):
  instruction = f"In this chat, respond as if you're explaining things to a {audience}. "
  question_msg = {
    "role": "user",
    "content": instruction + question
  }
  response = client.chat.completions.create(
    messages=[question_msg],
    model="gpt-3.5-turbo"
  )
  answer_msg = response.choices[0].message
  return answer_msg.content