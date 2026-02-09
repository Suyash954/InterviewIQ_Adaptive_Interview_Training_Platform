from django.urls import path
from .views import home, question_detail

urlpatterns = [
    path('', home, name='home'),
    path('question/<int:pk>/', question_detail, name='question_detail'),
]