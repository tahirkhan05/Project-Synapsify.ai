# Create your views here.

from django.shortcuts import render
from django.http import JsonResponse
from .gemini_chatbot import get_gemini_response
from .gpt_chatbot import get_gpt_response
from .groq_chatbot import get_groq_response
import os

chatbot_functions = {
    'gemini': get_gemini_response,
    'gpt': get_gpt_response,
    'groq': get_groq_response
}

chatbot_keys = {
    'gemini': 'GEMINI_API_KEY_',
    'gpt': 'OPENAI_API_KEY_',
    'groq': 'LLAMA_API_KEY_'
}

def index(request):
    return render(request, 'chatbot/test.html')

def get_response(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        responses = {}
        for i in range(1, 5):
            model_key = f'model-{i}'
            audience_key = f'audience-{i}'
            if model_key in request.POST:
                model = request.POST[model_key]
                audience = request.POST[audience_key]
                api_key = os.getenv(chatbot_keys[model] + str(i))
                response, _ = chatbot_functions[model](audience, prompt, api_key, [])
                responses[f'response{i}'] = response
        return JsonResponse(responses)
