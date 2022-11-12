from rest_framework import viewsets, mixins, permissions

from coreapp.models import Network
from coreapp.serializers import *
from coreapp.permissions import IsActive


class NetworkViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin
):
    """ViewSet for all Network objects"""
    queryset = Network.objects.all()
    serializer_class = None
    permission_classes = ()
    permissions_dict = {
        # 'list': (IsActive,),
        # 'retrieve': (IsActive,),
    }

    def get_permissions(self):
        if self.action in self.permissions_dict:
            perms = self.permissions_dict[self.action]
        else:
            perms = []
        return [permission() for permission in perms]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return NetworkSerializer
        return NetworkShortSerializer
