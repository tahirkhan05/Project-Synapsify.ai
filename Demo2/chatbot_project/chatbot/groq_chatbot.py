from groq import Groq

def get_groq_response(audience, question, api_key, history):
    client = Groq(api_key=api_key)
    instruction = f"In this chat, respond as if you're explaining things to a {audience}. "
    history.append({"role": "user", "content": instruction + question})
    response = client.chat.completions.create(
        messages=history,
        model="llama3-8b-8192"
    )
    answer_msg = response.choices[0].message
    history.append(answer_msg)
    return answer_msg.content, history
