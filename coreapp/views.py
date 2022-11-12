from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from coreapp.parameters import (country_parameter,
                                high_debt_parameter,
                                network_id_parameter,
                                product_id_parameter)
from coreapp.permissions import IsActive
from coreapp.serializers import *
from coreapp.services import filtering_unit_queryset


class NetworkViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin
):
    """Network objects listing"""
    queryset = Network.objects.all()
    serializer_class = NetworkSerializer
    # TODO permissions (IsActive,)
    permission_classes = ()


class UnitAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            network_id_parameter,
            country_parameter,
            product_id_parameter,
            high_debt_parameter
        ],
    )
    def get(self, request):
        queryset = filtering_unit_queryset(
            request,
            Unit.objects.all()
        )
        response_data = UnitShortSerializer(queryset, many=True).data
        return Response(response_data, status=200)
