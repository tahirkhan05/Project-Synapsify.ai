import google.generativeai as genai

def get_gemini_response(audience, question, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    chat = model.start_chat(history=[])
    instruction = f"In this chat, respond as if you're explaining things to a {audience}. "
    response = chat.send_message(instruction + question)
    return response.text
