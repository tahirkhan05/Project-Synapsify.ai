from groq import Groq

def get_groq_response(audience, question, api_key):
    client = Groq(api_key=api_key)
    instruction = f"In this chat, respond as if you're explaining things to a {audience}. "
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": instruction + question}],
        model="llama3-8b-8192"
    )
    answer_msg = response.choices[0].message
    return answer_msg.content
