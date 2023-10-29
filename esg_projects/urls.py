from rest_framework.routers import SimpleRouter

from .views import ESGProjectViewSet


router = SimpleRouter(trailing_slash=False)
router.register('esg_project', ESGProjectViewSet, basename="esg_project")


urlpatterns = router.get_urls()
