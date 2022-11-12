from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions


class IsActive(permissions.BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, AnonymousUser) and request.user.is_active
