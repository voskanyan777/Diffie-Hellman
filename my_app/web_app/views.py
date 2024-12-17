from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User, Session, AnonimMessage
from .token import generate_token
from .pass_hash import hash_password

DH_PARAMS = None
b = None
B = None
shared_secret = None
def index(request):
    global DH_PARAMS
    global b
    global B
    if DH_PARAMS is None:
        DH_PARAMS = {
            'p': 23,
            'g': 5
        }
        b = 15
        B = (DH_PARAMS['g'] ** b) % DH_PARAMS['p']


    # Создаем ответ и добавляем в него cookie
    response = render(request, 'index.html')
    # Добавляем данные DH_PARAMS в cookie
    response.set_cookie('p', DH_PARAMS['p'])
    response.set_cookie('g', DH_PARAMS['g'])

    return response
@csrf_exempt
def public_key(request):
    global shared_secret
    global B
    global b
    data = json.loads(request.body)
    client_public_key = data['public_key']
    shared_secret = (client_public_key**b) % 23
    print(f'Общий секрет на сервере: {shared_secret}')
    return JsonResponse(
        {
            'B': B
        }
    )


def login_page(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'registration.html')


def create_account(request):
    if request.method == "POST":
        login = request.POST['login']
        password = request.POST['password']
        password = hash_password(password)
        if User.objects.filter(login=login).exists():
            messages.error(request, 'Пользователь с таким логином существует')
            return redirect('register')
        user = User(login=login, password=password)
        user.save()

        return redirect('login')


def login(request):
    token = request.COOKIES.get('auth_token')
    if token:
        try:
            session = Session.objects.get(session_token=token)
            if session.token_is_valid():
                return redirect('messages')
            session.delete()
        except Session.DoesNotExist:
            pass
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
        password = hash_password(password)
        print(f"PASSWORD: {password}")
        try:
            user = User.objects.get(login=login, password=password)
            token = generate_token()
            session = Session(user=user, session_token=token)
            session.save()

            # Добавляем токен в куки
            response = redirect('messages')
            response.set_cookie('auth_token', token, httponly=True, secure=True, samesite='Strict')
            return response
        except User.DoesNotExist:
            messages.error(request, "Пользователь не найден")

    return render(request, 'login.html')

def messages(request):
    token = request.COOKIES.get('auth_token')
    if request.method == "GET":
        try:
            session = Session.objects.get(session_token=token)
            if not session.token_is_valid():
                return redirect('login')
            user = session.user
            message = AnonimMessage.objects.filter(user=user)
            return render(request, 'main.html', context={"messages_list": message})
        # Если токен не нашелся
        except Session.DoesNotExist:
            return redirect('login')

    return render(request, 'main.html')


def create_message(request):
    if request.method == "POST":
        login = request.POST.get('login')
        message = request.POST.get('message')
        try:
            user = User.objects.get(login=login)
            anon_message = AnonimMessage(user=user, message=message)
            anon_message.save()
            return redirect('create')
        except User.DoesNotExist:
            return redirect('create')
    return render(request, 'create-message.html')