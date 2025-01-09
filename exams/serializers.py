from rest_framework import serializers
from .models import Exam, Question, Option, StudentExam, StudentAnswer

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'option_text', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'options']

class ExamSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = ['id', 'title', 'created_by', 'created_at', 'questions']
        read_only_fields = ['created_by', 'created_at']

class CreateOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['option_text', 'is_correct']

class CreateQuestionSerializer(serializers.ModelSerializer):
    options = CreateOptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ['question_text', 'options']

    def create(self, validated_data):
        options_data = validated_data.pop('options')
        question = Question.objects.create(**validated_data)
        for option_data in options_data:
            Option.objects.create(question=question, **option_data)
        return question

class CreateExamSerializer(serializers.ModelSerializer):
    questions = CreateQuestionSerializer(many=True)

    class Meta:
        model = Exam
        fields = ['title', 'questions']

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        exam = Exam.objects.create(**validated_data)
        for question_data in questions_data:
            options_data = question_data.pop('options')
            question = Question.objects.create(exam=exam, **question_data)
            for option_data in options_data:
                Option.objects.create(question=question, **option_data)
        return exam

class StudentAnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    option_id = serializers.IntegerField(allow_null=True, required=False)

class ExamSubmissionSerializer(serializers.Serializer):
    exam_id = serializers.IntegerField()
    answers = StudentAnswerSerializer(many=True)

class StudentExamResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentExam
        fields = ['id', 'student', 'exam', 'score', 'total_questions', 'passed', 'taken_at']
        depth = 1