from django.db import models


class User(models.Model):
    login = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=350)

    class Meta:
        db_table = 'users'

