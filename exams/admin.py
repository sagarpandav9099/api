from django.contrib import admin
from .models import Exam, Question, Option, StudentExam, StudentAnswer

admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(StudentExam)
admin.site.register(StudentAnswer)