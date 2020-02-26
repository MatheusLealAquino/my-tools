from rest_framework import permissions
from django.contrib.auth.models import User

class IsAdvertiser(permissions.BasePermission):
  message = "Not authorized"

  def validate_permission(self, request, view, obj=None):
    if not request.user:
      return False

    if request.user.groups.filter(name='advertiser'):
      if obj is None:
        return True
      else:
        return request.user == obj.owner

    if request.method in permissions.SAFE_METHODS:
      if request.user.groups.filter(name='administrator') or request.user.is_superuser:
        return True
    return False

  def has_permission(self, request, view):
    return self.validate_permission(request, view)

  def has_object_permission(self, request, view, obj):
    return self.validate_permission(request, view, obj)