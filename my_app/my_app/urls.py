from django.contrib import admin
from django.urls import path
from web_app.views import index, login, register
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('login/', login),
    path('registration/', register),
]
