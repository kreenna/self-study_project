from rest_framework import permissions

from .models import Course, Lesson, Test


class IsCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsCourseCreator(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # для курсов проверяем, что пользователь является создателем или модератором
        if hasattr(obj, "user"):
            return obj.user == request.user
        return False

    def has_permission(self, request, view):

        if request.method == "POST":
            # для создания проверяем, что пользователь является создателем родительского курса
            if view.basename == "lesson":
                course_id = request.data.get("course")
                if not course_id:
                    return False

                try:
                    course = Course.objects.get(id=course_id)
                except Exception:
                    return False

                return course.user == request.user

            # также выполняем проверку для остальных моделей
            if view.basename == "test":
                lesson_id = request.data.get("lesson")
                if not lesson_id:
                    return False

                try:
                    lesson = Lesson.objects.get(id=lesson_id)
                except Exception:
                    return False

                course = lesson.course
                return course.user == request.user

            if view.basename == "question":
                test_id = request.data.get("test")

                if not test_id:
                    return False

                try:
                    test = Test.objects.get(id=test_id)
                except Exception:
                    return False

                lesson = test.lesson
                course = lesson.course
                return course.user == request.user

            if view.basename == "answer":
                test_id = request.data.get("test")
                if not test_id:
                    return False

                try:
                    test = Test.objects.get(id=test_id)
                except Exception:
                    return False

                lesson = test.lesson
                course = lesson.course
                return course.user == request.user

            # для других случаев нужна авторизация
            return request.user.is_authenticated

        # для остальных методов позволяем читать
        if request.method in permissions.SAFE_METHODS:
            return True

        return True
