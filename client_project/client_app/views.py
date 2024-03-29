# client_app/views.py

from django.shortcuts import redirect, render
from django.conf import settings
from django.http import HttpResponse
import requests
import os
import hashlib
import base64
import random
import string
from loguru import logger

def generate_code_verifier():
    """Генерирует случайный code verifier."""
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(43, 128)))

def generate_code_challenge(code_verifier):
    """Генерирует code challenge на основе code verifier."""
    code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(code_challenge).decode('utf-8').replace('=', '')

def login(request):
    """
    Отображает страницу входа.
    """
    return render(request, "login.html")

# В начале файла views.py добавьте:
STATE_CODE_VERIFIER_STORAGE = {}

def generate_state():
    """Генерирует уникальный state."""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(30))

# Измените функцию oauth2_login:
def oauth2_login(request):
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)
    state = generate_state()
    # Сохраняем code_verifier вместе с сгенерированным state
    STATE_CODE_VERIFIER_STORAGE[state] = code_verifier
    auth_url = f"{settings.OAUTH2_PROVIDER_URL}authorize/?client_id={settings.OAUTH2_CLIENT_ID}&response_type=code&redirect_uri={settings.OAUTH2_REDIRECT_URI}&scope=read introspection&code_challenge={code_challenge}&code_challenge_method=S256&state={state}"
    return redirect(auth_url)

# Измените функцию oauth2_callback:
def oauth2_callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    if code and state:
        code_verifier = STATE_CODE_VERIFIER_STORAGE.pop(state, '')
        # Оставшаяся часть функции остается без изменений

        token_url = f"{settings.OAUTH2_PROVIDER_URL}token/"
        logger.info(f"oauth2_callback - session_id: {request.session.session_key}, используемый code_verifier: {code_verifier}")

        token_data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': settings.OAUTH2_REDIRECT_URI,
            'client_id': settings.OAUTH2_CLIENT_ID,
            'client_secret': settings.OAUTH2_CLIENT_SECRET,
            'code_verifier': code_verifier,
        }
        token_response = requests.post(token_url, data=token_data)
        logger.info(f"Token response: {token_response.status_code} {token_response.text}")

        if token_response.status_code == 200:
            try:
                token_json = token_response.json()
                access_token = token_json.get('access_token')
                if access_token:
                    return HttpResponse(f"Access Token: Bearer {access_token}")
                else:
                    return HttpResponse("Error getting access token", status=400)
            except ValueError:
                return HttpResponse(f"Error decoding JSON: {token_response.text}", status=token_response.status_code)
        else:
            return HttpResponse(f"Error fetching token: {token_response.status_code} {token_response.text}", status=token_response.status_code)
    else:
        return HttpResponse("No code provided", status=400)
    


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class ExampleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)
    
    
from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer

class TaskListCreate(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

