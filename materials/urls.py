from rest_framework.routers import SimpleRouter

from materials.apps import MaterialsConfig

app_name = MaterialsConfig.name

router = SimpleRouter()

urlpatterns = [

]

urlpatterns += router.urls
