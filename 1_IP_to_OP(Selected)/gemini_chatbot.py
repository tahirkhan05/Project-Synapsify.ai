import google.generativeai as genai

def get_gemini_response(audience, question, api_key, history):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    # Convert the history to the required format
    gemini_history = []
    for h in history:
        if 'author' in h and 'content' in h:
            gemini_history.append({'role': h['author'], 'parts': [{'text': h['content']}]})
        elif 'role' in h and 'content' in h:
            gemini_history.append({'role': h['role'], 'parts': [{'text': h['content']}]})

    chat = model.start_chat(history=gemini_history)
    instruction = f"In this chat, respond as if you're explaining things to a {audience}. "
    response = chat.send_message(instruction + question)
    
    history.append({"role": "user", "content": instruction + question})
    history.append({"role": "model", "content": response.text})
    return response.text, history
