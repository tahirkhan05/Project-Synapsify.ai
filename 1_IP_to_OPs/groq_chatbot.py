import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('LLAMA_API_KEY')

client = Groq(
  api_key=API_KEY
)

history = []

def get_groq_response(audience, question):
    instruction = f"In this chat, respond as if you're explaining things to a {audience}. "
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": instruction + question}],
        model="llama3-8b-8192"
    )
    answer_msg = response.choices[0].message
    return answer_msg.content
