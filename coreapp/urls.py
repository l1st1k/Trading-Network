from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'network', NetworkViewSet, basename='network')

urlpatterns = [
    path('units', UnitAPIView.as_view(), name='units'),
]
urlpatterns += router.urls
