from django.urls import path
from .views import (
    CreateExamView, 
    ExamListView, 
    ExamSubmissionView, 
    StudentExamResultView
)

urlpatterns = [
    path('create/', CreateExamView.as_view(), name='create_exam'),
    path('list/', ExamListView.as_view(), name='exam_list'),
    path('submit/', ExamSubmissionView.as_view(), name='exam_submission'),
    path('results/', StudentExamResultView.as_view(), name='exam_results'),
]