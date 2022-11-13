from datetime import datetime

from rest_framework import viewsets, status
from rest_framework.response import Response

from coreapp.models import Product
from coreapp.serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet for all actions with Products"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        product_data = request.data
        if Product.objects.filter(name=product_data['name']).exists():
            return Response(
                {"There is already a product with the same name! Please, try another."},
                status=status.HTTP_409_CONFLICT
            )
        release_time = product_data['release_date']
        now: str = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        if not release_time > now:
            return Response(
                {"Incorrect release_date!"},
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
        new_product = Product.objects.create(
            name=product_data['name'],
            model=product_data['model'],
            release_date=product_data['release_date']
        )
        new_product.save()
        serializer = self.serializer_class(new_product)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
