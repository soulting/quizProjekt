from rest_framework import routers
from .views import UsersViewSet, QuizViewSet, QuestionViewSet
from django.urls import include, path

router = routers.DefaultRouter()
router.register(r'quiz', QuizViewSet)
router.register(r'question', QuestionViewSet)
router.register(r'users', UsersViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
