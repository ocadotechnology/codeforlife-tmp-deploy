from rest_framework.permissions import AllowAny as _AllowAny
from rest_framework.permissions import BasePermission as _BasePermission


class BasePermission(_BasePermission):
    """Base permission which all other permissions must inherit from."""

    def __eq__(self, other):
        return isinstance(other, self.__class__)


class AllowAny(BasePermission, _AllowAny):
    """Allows all incoming requests."""
