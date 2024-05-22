from groq import Groq
import logging

def get_groq_response(audience, language, question, api_key, history):
    try:
        client = Groq(api_key=api_key)
        instruction = f"In this chat, respond as if you're explaining things to a {audience} in {language} language. "
        history.append({"role": "user", "content": instruction + question})
        response = client.chat.completions.create(
            messages=history,
            model="llama3-8b-8192"
        )
        answer_msg = response.choices[0].message
        history.append(answer_msg)
        return answer_msg.content, history
    except Exception as e:
        logging.error(f"Failed to get response from Groq: {e}")
        return "An error occurred while fetching the response. Please try again later.", history
