from rest_framework import serializers

from .models import Course, Lesson, Test, Question, Answer, Choice


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "title", "description", "course", "user"]


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ["id", "title", "description", "lessons", "user"]


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ["id", "topic", "lesson"]


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "content", "test"]


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "content", "test", "is_correct"]


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ["id", "question", "chosen_answer", "is_right"]
