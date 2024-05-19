from openai import OpenAI

def get_gpt_response(audience, question, api_key):
    client = OpenAI(api_key=api_key)
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
