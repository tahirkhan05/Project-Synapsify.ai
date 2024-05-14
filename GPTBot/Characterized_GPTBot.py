import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(
  api_key=API_KEY
)

history = []
system_msg = {
  "role": "system",
  "content": "respond as if you're explaining things to a professional coder."
}
history.append(system_msg)

def ask(question):
  question_msg = {
    "role": "user",
    "content": question
  }
  history.append(question_msg)
  response = client.chat.completions.create(
    messages=history,
    model="gpt-3.5-turbo"
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
  print(f"GPT: {answer}")
  print('\n')