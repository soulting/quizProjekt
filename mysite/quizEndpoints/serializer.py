from .models import Quiz, Question, Users
from rest_framework import serializers


class QuizSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'icon', 'color']


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ['quiz', 'question', 'option_a', 'option_b', 'option_c', 'option_d', 'answer', 'explanation']


class UsersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'password', 'quiz_ids', 'is_admin', 'icon_name']
