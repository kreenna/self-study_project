from rest_framework.routers import SimpleRouter

from materials.apps import MaterialsConfig
from materials.views import CourseViewSet, LessonViewSet, TestViewSet, QuestionViewSet, AnswerViewSet, ChoiceViewSet

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'lessons', LessonViewSet, basename='lessons')
router.register(r'tests', TestViewSet, basename='test')
router.register(r'questions', QuestionViewSet, basename='questions')
router.register(r'answers', AnswerViewSet, basename='answers')
router.register(r'choices', ChoiceViewSet, basename='choices')

urlpatterns = router.urls
