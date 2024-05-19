from django.shortcuts import render
from django.http import JsonResponse
from .chatbot_handlers import get_response_from_chatbot

# Create your views here.

def index(request):
    return render(request, 'index.html')

def get_response(request):
    if request.method == "POST":
        prompt = request.POST.get('prompt')
        audience = request.POST.get('audience')
        model = request.POST.get('model')
        response = get_response_from_chatbot(model, audience, prompt)
        return JsonResponse({'response': response})