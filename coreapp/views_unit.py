from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.response import Response

from coreapp.models import Unit
from coreapp.parameters import (country_parameter,
                                high_debt_parameter,
                                network_id_parameter,
                                product_id_parameter)
from coreapp.permissions import IsActive, IsUnitMember
from coreapp.serializers import (UnitNoDebtSerializer,
                                 UnitSerializer,
                                 UnitShortSerializer)
from coreapp.services import filtering_unit_queryset


class UnitViewSet(viewsets.ModelViewSet):
    """ViewSet for all actions with Units"""
    queryset = Unit.objects.all()
    permission_classes = []
    serializer_class = None
    # TODO permissions (after JWT, cause swagger is always AnonymousUser)

    # permissions_dict = {
    #     'partial_update': (IsActive, IsUnitMember),
    #     'update': (IsActive, IsUnitMember),
    #     'destroy': (IsActive, IsUnitMember),
    #     'create': (IsActive,),
    #     'list': (IsActive,),
    #     'retrieve': (IsActive, IsUnitMember),
    # }
    #
    # # a method that set permissions depending on http request methods
    # # very useful in case of adding new permissions to actions
    # def get_permissions(self):
    #     if self.action in self.permissions_dict:
    #         perms = self.permissions_dict[self.action]
    #     else:
    #         perms = []
    #     return [permission() for permission in perms]
    #
    # def check_permissions(self, request):
    #     try:
    #         obj = Unit.objects.get(id=self.kwargs.get('pk'))
    #     except Unit.DoesNotExist:
    #         return Response({'message': 'Unit not found!'}, status.HTTP_404_NOT_FOUND)
    #     else:
    #         self.check_object_permissions(request, obj)
    #     finally:
    #         return super().check_permissions(request)

    def get_serializer_class(self):
        return UnitSerializer if self.action == 'retrieve' else UnitNoDebtSerializer

    @swagger_auto_schema(
        manual_parameters=[
            network_id_parameter,
            country_parameter,
            product_id_parameter,
            high_debt_parameter
        ],
    )
    def list(self, request, *args, **kwargs):
        queryset = filtering_unit_queryset(
            request,
            Unit.objects.all()
        )
        response_data = UnitShortSerializer(queryset, many=True).data
        return Response(response_data, status=status.HTTP_200_OK)
