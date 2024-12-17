from django.contrib import admin
from django.urls import path
from web_app.views import (index, login_page, register, create_account, login,
                           messages)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('login_page/', login, name='login'),
    path('registration/', register, name='register'),
    path('register-account/', create_account),
    path('login/', login),
    path('messages/', messages, name='messages'),
]
