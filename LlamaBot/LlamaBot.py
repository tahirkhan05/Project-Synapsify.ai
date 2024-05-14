import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('LLAMA_API_KEY')

client = Groq(
  api_key = API_KEY
)
history = []

def ask(question):
  question_msg = {
    "role": "user",
    "content": question
  }
  history.append(question_msg)
  response = client.chat.completions.create(
    messages=history,
    model="llama3-8b-8192"
  )
  answer_msg = response.choices[0].message
  history.append(answer_msg)
  return answer_msg.content

while(True):
  question = input("You: ")

  if(question.strip() == ''):
    break

  answer = ask(question)
  print('\n')
  print(f"Llama3: {answer}")
  print('\n')
