from rest_framework import mixins, viewsets

from coreapp.models import Network
from coreapp.permissions import IsActive
from coreapp.serializers import NetworkSerializer, NetworkShortSerializer


class NetworkViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin
):
    """Viewset for actions with Network objects"""
    queryset = Network.objects.all()
    serializer_class = None
    permission_classes = (IsActive,)

    def get_serializer_class(self):
        return NetworkShortSerializer if self.action == 'list' else NetworkSerializer
