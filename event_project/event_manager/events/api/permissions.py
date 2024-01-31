""" 
Eigene Permisson erstellen: Nur der AdminUser darf schreiben (POST, PUT, PATCH), alle anderen
dürfen lesen (SAVE_METHODS)

"""
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    """
    The request is authenticated as a admin user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_superuser
        )