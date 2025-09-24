from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from materials.models import Course, Lesson, Test, Question, Answer, Choice

User = get_user_model()


class MaterialsPermissionsTest(APITestCase):

    def setUp(self):
        # создаем пользователей
        self.creator = User.objects.create_user(username="creator", email="creator@gmail.com", password="pass")
        self.moderator = User.objects.create_user(username="moderator", email="mod@gmail.com", password="pass",
                                                  is_staff=True)
        self.other_user = User.objects.create_user(username="other", email="other@gmail.com", password="pass")

        # аутентификация для каждого пользователя
        self.client_creator = APIClient()
        self.client_creator.force_authenticate(user=self.creator)

        self.client_moderator = APIClient()
        self.client_moderator.force_authenticate(user=self.moderator)

        self.client_other = APIClient()
        self.client_other.force_authenticate(user=self.other_user)

        # создаем модели
        self.course = Course.objects.create(title="Course 1", description="Desc", user=self.creator)
        self.lesson = Lesson.objects.create(title="Lesson 1", description="Desc", course=self.course,
                                            user=self.creator)
        self.test = Test.objects.create(topic="Test Topic", lesson=self.lesson, user=self.creator)
        self.question = Question.objects.create(content="Question?", test=self.test, user=self.creator)
        self.answer = Answer.objects.create(content="Answer", test=self.test, is_correct=True, user=self.creator)
        self.choice = Choice.objects.create(question=self.question, chosen_answer=self.answer, is_right=False,
                                            user=self.creator)

    # метод для помощи тестам в получении данных
    def crud_tests(self, base_url_name, data_create, data_update, obj_id=None):
        list_url = f"/materials/{base_url_name}/"
        detail_url = f"/materials/{base_url_name}/{obj_id}/"

        # любой пользователь может просматривать
        list_response_creator = self.client_creator.get(list_url)
        self.assertEqual(list_response_creator.status_code, status.HTTP_200_OK)
        list_response_other = self.client_other.get(list_url)
        self.assertEqual(list_response_other.status_code, status.HTTP_200_OK)

        # создание доступно для всех авторизованных пользователей
        create_resp_creator = self.client_creator.post(list_url, data_create)
        self.assertIn(create_resp_creator.status_code, [status.HTTP_201_CREATED,
                                                        status.HTTP_400_BAD_REQUEST])
        create_resp_moderator = self.client_moderator.post(list_url, data_create)
        self.assertIn(create_resp_moderator.status_code, [status.HTTP_201_CREATED,
                                                          status.HTTP_400_BAD_REQUEST])
        create_resp_other = self.client_other.post(list_url, data_create)
        self.assertIn(create_resp_other.status_code, [status.HTTP_201_CREATED,
                                                      status.HTTP_400_BAD_REQUEST])

        if obj_id is None:
            return

        # получение доступно для всех авторизовавшихся пользователей
        self.assertEqual(self.client_creator.get(detail_url).status_code, status.HTTP_200_OK)
        self.assertEqual(self.client_other.get(detail_url).status_code, status.HTTP_200_OK)

        # обновление доступно для модераторов или создателей
        resp_creator = self.client_creator.put(detail_url, data_update)
        self.assertIn(resp_creator.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])
        resp_moderator = self.client_moderator.put(detail_url, data_update)
        self.assertIn(resp_moderator.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])
        resp_other = self.client_other.put(detail_url, data_update)
        self.assertEqual(resp_other.status_code, status.HTTP_403_FORBIDDEN)

        # частичное обновление доступно для модераторов или создателей
        patch_data = {k: v for k, v in data_update.items() if isinstance(v, str)}
        resp_patch_creator = self.client_creator.patch(detail_url, patch_data)
        self.assertIn(resp_patch_creator.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])
        resp_patch_other = self.client_other.patch(detail_url, patch_data)
        self.assertEqual(resp_patch_other.status_code, status.HTTP_403_FORBIDDEN)

        # удаление доступно для модераторов или создателей
        resp_delete_creator = self.client_creator.delete(detail_url)
        self.assertIn(resp_delete_creator.status_code, [status.HTTP_204_NO_CONTENT, status.HTTP_404_NOT_FOUND])
        resp_delete_moderator = self.client_moderator.delete(detail_url)
        self.assertIn(resp_delete_moderator.status_code, [status.HTTP_204_NO_CONTENT,
                                                          status.HTTP_404_NOT_FOUND])
        resp_delete_other = self.client_other.delete(detail_url)
        self.assertEqual(resp_delete_other.status_code, status.HTTP_404_NOT_FOUND)

    def test_course_crud(self):
        create_data = {"title": "New course", "description": "desc"}
        update_data = {"title": "Updated course", "description": "updated desc"}
        self.crud_tests("courses", create_data, update_data, self.course.pk)

    def test_lesson_crud(self):
        create_data = {"title": "New lesson", "description": "desc", "course": self.course.pk}
        update_data = {"title": "Updated lesson", "description": "updated desc",
                       "course": self.course.pk}
        self.crud_tests("lessons", data_create=create_data, data_update=update_data,
                        obj_id=self.lesson.pk)

    def test_test_crud(self):
        create_data = {"topic": "New test", "lesson": self.lesson.pk}
        update_data = {"topic": "Updated test", "lesson": self.lesson.pk}
        self.crud_tests("tests", data_create=create_data, data_update=update_data, obj_id=self.test.pk)

    def test_question_crud(self):
        create_data = {"content": "New question", "test": self.test.pk}
        update_data = {"content": "Updated question", "test": self.test.pk}
        self.crud_tests("questions", data_create=create_data, data_update=update_data,
                        obj_id=self.question.pk)

    def test_answer_crud(self):
        create_data = {"content": "New answer", "test": self.test.pk, "is_correct": False}
        update_data = {"content": "Updated answer", "test": self.test.pk, "is_correct": False}
        self.crud_tests("answers", data_create=create_data, data_update=update_data, obj_id=self.answer.pk)


class ChoiceViewSetTest(APITestCase):
    def setUp(self):
        # создаем пользователей
        self.creator = User.objects.create_user(username="creator", email="creator@example.com", password="testpass")
        self.other_user = User.objects.create_user(username="other", email="other@example.com", password="testpass")

        # аутентификация создателя
        self.client_creator = APIClient()
        self.client_creator.force_authenticate(user=self.creator)

        # аутентификацияя другого пользователя
        self.client_other = APIClient()
        self.client_other.force_authenticate(user=self.other_user)

        # создаем модели создателя
        self.course = Course.objects.create(title="Course 1", description="desc", user=self.creator)
        self.lesson = Lesson.objects.create(title="Lesson 1", description="desc", course=self.course,
                                            user=self.creator)
        self.test = Test.objects.create(topic="Test topic", lesson=self.lesson, user=self.creator)
        self.question = Question.objects.create(content="Question?", test=self.test, user=self.creator)
        self.answer = Answer.objects.create(content="Answer", test=self.test, is_correct=True, user=self.creator)

        # создаем выбор создателя
        self.choice = Choice.objects.create(question=self.question, chosen_answer=self.answer, is_right=True,
                                            user=self.creator)

        self.list_url = "/materials/choices/"
        self.detail_url = f"/materials/choices/{self.choice.pk}/"

    def test_list_choices(self):
        # авторизованные пользователи могут просматривать
        response = self.client_creator.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_choice(self):
        data = {
            "question": self.question.pk,
            "chosen_answer": self.answer.pk
        }
        response = self.client_creator.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data.get("is_right"))

    def test_retrieve_choice_by_creator(self):
        response = self.client_creator.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_choice_by_creator(self):
        data = {
            "question": self.question.pk,
            "chosen_answer": self.answer.pk,
            "is_right": False  # attempt update
        }
        response = self.client_creator.put(self.detail_url, data)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])

    def test_partial_update_choice_by_creator(self):
        data = {
            "is_right": False
        }
        response = self.client_creator.patch(self.detail_url, data)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])

    def test_update_choice_by_other_forbidden(self):
        data = {
            "is_right": False
        }
        response = self.client_other.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_choice_by_creator(self):
        response = self.client_creator.delete(self.detail_url)
        self.assertIn(response.status_code, [status.HTTP_204_NO_CONTENT, status.HTTP_404_NOT_FOUND])

    def test_delete_choice_by_other_forbidden(self):
        response = self.client_other.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
