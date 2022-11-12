from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from coreapp.serializers import *
from coreapp.permissions import IsActive
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
    def get(self, request):
        # TODO swagger schema for query params
        queryset = filtering_unit_queryset(
            request,
            Unit.objects.all()
        )
        response_data = UnitShortSerializer(queryset, many=True).data
        return Response(response_data, status=200)
