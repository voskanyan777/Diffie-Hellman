# Generated by Django 5.1.4 on 2024-12-17 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0002_session_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='anonimmessage',
            name='date',
        ),
    ]
