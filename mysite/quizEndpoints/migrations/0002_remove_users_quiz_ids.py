# Generated by Django 5.0 on 2024-01-05 10:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizEndpoints', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='quiz_ids',
        ),
    ]
