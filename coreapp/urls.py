from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'network', NetworkViewSet, basename='network')
urlpatterns = router.urls
