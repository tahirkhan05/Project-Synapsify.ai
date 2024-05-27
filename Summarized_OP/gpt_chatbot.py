from openai import OpenAI
import logging

def get_gpt_response(audience, language, question, api_key, history):
    try:
        client = OpenAI(api_key=api_key)
        instruction = f"In this chat, respond as if you're explaining things to a {audience} in {language} language. "
        question_msg = {
            "role": "user",
            "content": instruction + question
        }
        history.append(question_msg)
        response = client.chat.completions.create(
            messages=history,
            model="gpt-3.5-turbo"
        )
        answer_msg = response.choices[0].message
        history.append(answer_msg)
        return answer_msg.content, history
    except Exception as e:
        logging.error(f"Failed to get response from GPT: {e}")
        return "An error occurred while fetching the response. Please try again later.", history
