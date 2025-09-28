from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsModerator
from .models import Course, Lesson, Test, Question, Answer, Choice
from .permissions import IsCreator, IsCourseCreator
from .serializers import (CourseSerializer, LessonSerializer, TestSerializer, QuestionSerializer, AnswerSerializer,
                          ChoiceSerializer)


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ["update", "partial_update"]:
            self.permission_classes = [IsAuthenticated, IsModerator | IsCourseCreator]
        elif self.action in ["destroy"]:
            self.permission_classes = [IsAuthenticated, IsModerator | IsCourseCreator]
        else:
            self.permission_classes = [IsAuthenticated]

        return [permission() for permission in self.permission_classes]


class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ["update", "partial_update"]:
            self.permission_classes = [IsAuthenticated, IsModerator | IsCourseCreator]
        elif self.action in ["destroy"]:
            self.permission_classes = [IsAuthenticated, IsModerator | IsCourseCreator]
        else:
            self.permission_classes = [IsAuthenticated]

        return [permission() for permission in self.permission_classes]


class TestViewSet(viewsets.ModelViewSet):
    serializer_class = TestSerializer
    queryset = Test.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ["update", "partial_update"]:
            self.permission_classes = [IsAuthenticated, IsModerator | IsCourseCreator]
        elif self.action in ["destroy"]:
            self.permission_classes = [IsAuthenticated, IsModerator | IsCourseCreator]
        else:
            self.permission_classes = [IsAuthenticated]

        return [permission() for permission in self.permission_classes]


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ["update", "partial_update"]:
            self.permission_classes = [IsAuthenticated, IsModerator | IsCourseCreator]
        elif self.action in ["destroy"]:
            self.permission_classes = [IsAuthenticated, IsModerator | IsCourseCreator]
        else:
            self.permission_classes = [IsAuthenticated]

        return [permission() for permission in self.permission_classes]


class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ["update", "partial_update"]:
            self.permission_classes = [IsAuthenticated, IsModerator | IsCourseCreator]
        elif self.action in ["destroy"]:
            self.permission_classes = [IsAuthenticated, IsModerator | IsCourseCreator]
        else:
            self.permission_classes = [IsAuthenticated]

        return [permission() for permission in self.permission_classes]


class ChoiceViewSet(viewsets.ModelViewSet):
    serializer_class = ChoiceSerializer
    queryset = Choice.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        question = serializer.validated_data.get("question")
        chosen_answer = serializer.validated_data.get("chosen_answer")
        if chosen_answer.is_correct and question == chosen_answer.question:
            is_right = True
        else:
            is_right = False
        serializer.save(user=self.request.user, question=question, chosen_answer=chosen_answer, is_right=is_right)

    def get_permissions(self):
        if self.action in ["update", "partial_update"]:
            self.permission_classes = [IsAuthenticated, IsCreator]
        elif self.action in ["destroy"]:
            self.permission_classes = [IsAuthenticated, IsCreator]
        else:
            self.permission_classes = [IsAuthenticated]

        return [permission() for permission in self.permission_classes]
