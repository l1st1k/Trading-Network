from rest_framework import viewsets

from coreapp.models import Product
from coreapp.serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet for all actions with Products"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
