from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Session, AnonimMessage
from .token import generate_token
from .pass_hash import hash_password
def index(request):
    return render(request, 'index.html')


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