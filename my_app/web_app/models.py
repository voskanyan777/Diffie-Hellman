from django.db import models
from django.utils import timezone
from datetime import timedelta

class User(models.Model):
    login = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=350)

    class Meta:
        db_table = 'users'


class AnonimMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()

    class Meta:
        db_table = 'anon_message'


class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sessions'

    def token_is_valid(self):
        return self.created_at > timezone.now() - timedelta(minutes=15)
