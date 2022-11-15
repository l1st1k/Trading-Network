from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions


class IsActive(permissions.BasePermission):
    def has_permission(self, request, view):
        return not isinstance(request.user, AnonymousUser) and request.user.is_active


class IsUnitMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.members.all()
