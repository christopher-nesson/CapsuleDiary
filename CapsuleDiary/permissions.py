"""
Master:Chao
Datetime:2021/1/8 14:05
Reversion:1.0
File: permissions.py
"""
from rest_framework.permissions import BasePermission


class IsSuperAdminUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)
