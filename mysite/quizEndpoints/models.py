from django.db import models


# Create your models here.
class Question(models.Model):
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)  # Relacja z tabelą quizzes
    question = models.CharField(max_length=255)
    option_a = models.CharField(max_length=255, blank=True, null=True)
    option_b = models.CharField(max_length=255, blank=True, null=True)
    option_c = models.CharField(max_length=255, blank=True, null=True)
    option_d = models.CharField(max_length=255, blank=True, null=True)
    answer = models.CharField(max_length=255)
    explanation = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.question


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=255, blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.title


class Users(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    quiz_ids = models.JSONField(blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    icon_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username
