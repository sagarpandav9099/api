from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from .models import Exam, Question, Option, StudentExam, StudentAnswer
from .serializers import (
    ExamSerializer, 
    CreateExamSerializer, 
    ExamSubmissionSerializer, 
    StudentExamResultSerializer
)

class CreateExamView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Only admin can create exam
        if request.user.role != 'admin':
            return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)

        serializer = CreateExamSerializer(data=request.data)
        if serializer.is_valid():
            exam = serializer.save(created_by=request.user)
            return Response(ExamSerializer(exam).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExamListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        exams = Exam.objects.all()
        serializer = ExamSerializer(exams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ExamSubmissionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Students (and possibly admins, but typically students) submit
        serializer = ExamSubmissionSerializer(data=request.data)
        if serializer.is_valid():
            exam_id = serializer.validated_data['exam_id']
            answers_data = serializer.validated_data['answers']

            exam = get_object_or_404(Exam, id=exam_id)
            student_exam = StudentExam.objects.create(
                student=request.user,
                exam=exam,
                total_questions=exam.questions.count()
            )

            correct_count = 0
            for ans in answers_data:
                question_id = ans['question_id']
                option_id = ans.get('option_id', None)

                question = get_object_or_404(Question, id=question_id, exam=exam)

                chosen_option = None
                if option_id is not None:
                    chosen_option = get_object_or_404(Option, id=option_id, question=question)
                
                StudentAnswer.objects.create(
                    student_exam=student_exam,
                    question=question,
                    chosen_option=chosen_option
                )

                # Check correctness
                if chosen_option and chosen_option.is_correct:
                    correct_count += 1

            # Calculate score, pass/fail
            student_exam.score = correct_count
            pass_mark = student_exam.total_questions * 0.5  # 50%
            student_exam.passed = (correct_count >= pass_mark)
            student_exam.save()

            return Response({
                "message": "Exam submitted successfully",
                "score": student_exam.score,
                "total": student_exam.total_questions,
                "passed": student_exam.passed
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentExamResultView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role == 'admin':
            # Admin can see all results
            exams = StudentExam.objects.all()
        else:
            # Student can only see their results
            exams = StudentExam.objects.filter(student=request.user)

        serializer = StudentExamResultSerializer(exams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)