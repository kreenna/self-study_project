from django.db import models

from config.settings import AUTH_USER_MODEL


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="courses",
                             verbose_name="Создатель")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    title = models.CharField(max_length=250, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс")
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="lessons",
                             verbose_name="Создатель")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Test(models.Model):
    topic = models.CharField(max_length=200, verbose_name="Тема")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="tests", verbose_name="Урок")
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tests",
                             verbose_name="Создатель")

    def __str__(self):
        return self.topic

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"


class Question(models.Model):
    content = models.TextField(verbose_name="Вопрос")
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="questions", verbose_name="Тест")
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="questions",
                             verbose_name="Создатель")

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class Answer(models.Model):
    content = models.TextField(verbose_name="Вариант ответа")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers", verbose_name="Вопрос")
    is_correct = models.BooleanField(default=False)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="answers",
                             verbose_name="Создатель")

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="question", verbose_name="Вопрос")
    chosen_answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="answer", verbose_name="Ответ")
    is_right = models.BooleanField(default=False)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="choices",
                             verbose_name="Ответчик")

    class Meta:
        verbose_name = "Выбор"
        verbose_name_plural = "Выборы"
