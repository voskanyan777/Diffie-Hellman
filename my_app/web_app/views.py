from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User, Session, AnonimMessage
from .token import generate_token
from .pass_hash import hash_password
from .dh_alg import DHAlgorithm, decrypt_message

dh = DHAlgorithm()

def index(request):
    # Если общий ключ еще не сгенерирован
    if dh.shared_key is None:
        dh.public_key()  # Генерация публичного ключа сервера
        return render(request, 'index.html', {'clear_localstorage': True})
    return render(request,'index.html')


def login_page(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'registration.html')


def create_account(request):
    if request.method == "POST":
        login = request.POST['login']
        password = request.POST['password']

        print(f'Зашифрованный логин: {login}')
        print(f'Зашифрованный пароль: {password}')


        login = decrypt_message(login, dh.shared_key)
        password = decrypt_message(password, dh.shared_key)


        print(f'Расшифрованный логин: {login}')
        print(f'Расшифрованный пароль: {password}')

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
                return render(request, "main.html", {'user_is_auth': True})
            session.delete()
        except Session.DoesNotExist:
            pass
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')

        print(f'Зашифрованный логин: {login}')
        print(f'Зашифрованный пароль: {password}')


        login = decrypt_message(login, dh.shared_key)
        password = decrypt_message(password, dh.shared_key)


        print(f'Расшифрованный логин: {login}')
        print(f'Расшифрованный пароль: {password}')

        password = hash_password(password)

        try:
            user = User.objects.get(login=login, password=password)
            token = generate_token()
            session = Session(user=user, session_token=token)
            session.save()

            response = redirect('messages')
            response.set_cookie('auth_token', token, httponly=True, secure=True, samesite='Strict')
            return response
        except User.DoesNotExist:
            messages.error(request, "Пользователь не найден")

    return render(request, 'login.html')

def user_messages(request):
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

        print(f'Зашифрованный логин: {login}')
        print(f'Зашифрованное сообщение: {message}')

        login = decrypt_message(login, dh.shared_key)
        message = decrypt_message(message, dh.shared_key)

        print(f'Расшифрованный логин: {login}')
        print(f'Расшифрованное сообщение: {message}')

        try:
            user = User.objects.get(login=login)
            anon_message = AnonimMessage(user=user, message=message)
            anon_message.save()
            return redirect('create')
        except User.DoesNotExist:
            messages.error(request, "Пользователь с таким логином не найден")
            return redirect('create')
    if request.method == "GET":
        token = request.COOKIES.get('auth_token')
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

@csrf_exempt
def public_keys(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            server_public_key = data.get('public_key')
            dh.shared_key = int(server_public_key, 10)
            print(f'ОБЩИЙ СЕКРЕТНЫЙ КЛЮЧ {dh.shared_key}')

            return JsonResponse({'public_key': str(dh.server_public_key)})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

def logout(request):
    response = redirect('index')
    response.delete_cookie('auth_token', path='/', samesite='Strict')
    return response