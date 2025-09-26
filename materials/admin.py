from django.contrib import admin

from .models import Course, Lesson, Test, Question, Answer, Choice


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "description")
    search_fields = ("id", "user")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "description", "course")
    search_fields = ("id", "user", "course")


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "topic", "lesson")
    search_fields = ("id", "user")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "test", "content")
    search_fields = ("id", "user", "content")


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "test", "content", "is_correct")
    list_filter = ("is_correct",)
    search_fields = ("id", "user", "content")


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "question", "chosen_answer", "is_right")
    list_filter = ("is_right",)
    search_fields = ("id", "user")
