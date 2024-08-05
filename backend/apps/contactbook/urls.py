from rest_framework.routers import DefaultRouter

from apps.contactbook.views import ContactBookViewSet

app_name = "contactbook"
router = DefaultRouter()
router.register("", ContactBookViewSet)

urlpatterns = router.urls
