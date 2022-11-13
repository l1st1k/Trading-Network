from rest_framework.routers import DefaultRouter

from coreapp.views_network import NetworkViewSet
from coreapp.views_product import ProductViewSet
from coreapp.views_unit import UnitViewSet

router = DefaultRouter()
router.register(r'networks', NetworkViewSet, basename='network')
router.register(r'units', UnitViewSet, basename='units')
router.register(r'products', ProductViewSet, basename='products')

urlpatterns = router.urls
