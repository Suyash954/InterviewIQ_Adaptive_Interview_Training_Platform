
from django.db import models
from django.contrib.auth.models import User

class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Question(models.Model):
    question_text = models.TextField()
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=20)

    def __str__(self):
        return self.question_text[:50]

class Attempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
