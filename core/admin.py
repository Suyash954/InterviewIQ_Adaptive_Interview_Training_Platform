from django.contrib import admin
from .models import Skill, Question, Attempt
admin.site.register(Skill)
admin.site.register(Question)
admin.site.register(Attempt)