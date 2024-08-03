from rest_framework.routers import DefaultRouter

from label.views import LabelViewSet

app_name = "label"
router = DefaultRouter()

router.register("", LabelViewSet)
urlpatterns = router.urls
