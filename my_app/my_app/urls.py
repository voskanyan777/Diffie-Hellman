from django.contrib import admin
from django.urls import path
from web_app.views import (index, create_message, register, create_account, login,
                           messages, public_key)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('login_page/', login, name='login'),
    path('registration/', register, name='register'),
    path('register-account/', create_account),
    path('login/', login),
    path('messages/', messages, name='messages'),
    path('create/', create_message, name='create'),
    path('public-key/', public_key),
]
