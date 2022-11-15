from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from coreapp.models import Unit
from coreapp.parameters import (country_parameter, high_debt_parameter,
                                network_id_parameter, product_id_parameter)
from coreapp.permissions import IsActive, IsUnitMember
from coreapp.serializers import (UnitContactsSerializer, UnitNoDebtSerializer,
                                 UnitSerializer, UnitShortSerializer)
from coreapp.services import filtering_unit_queryset
from coreapp.tasks import celery_create_and_send_qr


class UnitViewSet(viewsets.ModelViewSet):
    """ViewSet for all actions with Units"""
    queryset = Unit.objects.all()
    permission_classes = []
    serializer_class = None

    permissions_dict = {
        'list': (IsActive,),
        'create': (IsActive,),
        'retrieve': (IsActive, IsUnitMember),
        'partial_update': (IsActive, IsUnitMember),
        'update': (IsActive, IsUnitMember),
        'destroy': (IsActive, IsUnitMember),
        'qr': (IsActive, IsUnitMember),
    }

    # a method that set permissions depending on http request methods
    # very useful in case of adding new permissions to actions
    def get_permissions(self):
        if self.action in self.permissions_dict:
            perms = self.permissions_dict[self.action]
        else:
            perms = []
        return [permission() for permission in perms]

    def check_permissions(self, request):
        try:
            obj = Unit.objects.get(id=self.kwargs.get('pk'))
        except Unit.DoesNotExist:
            return Response({'message': 'Unit not found!'}, status.HTTP_404_NOT_FOUND)
        else:
            self.check_object_permissions(request, obj)
        finally:
            return super().check_permissions(request)

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
        # Filtering via query params
        queryset = filtering_unit_queryset(
            request,
            Unit.objects.all()
        )

        # Serializing data
        response_data = UnitShortSerializer(queryset, many=True).data
        return Response(response_data, status=status.HTTP_200_OK)

    @action(detail=True, methods=('get',))
    def qr(self, request, *args, **kwargs):
        unit = self.get_object()

        # Getting user contacts
        data = UnitContactsSerializer(unit).data

        # Creating QR-code and sending it to user email
        # TODO add .delay (celery)
        # Should be with '.delay', as below, but for now it removed for test needs.
        # p.s. haven't separated celery worker
        # celery_create_and_send_qr.delay(request.user.email, data)
        celery_create_and_send_qr(request.user.email, data)

        return Response(f'QR-code successfully sent!', status=status.HTTP_200_OK)
