from rest_framework import permissions
from django.contrib.auth.models import User

class IsAdvertiser(permissions.BasePermission):
  message = "Not an advertiser."

  def has_object_permission(self, request, view, obj):
    if not request.user:
      return False

    user = User.objects.get(username=request.user)
    if user.groups.filter(name='advertiser'):
      return request.user == obj.owner

    if request.method in permissions.SAFE_METHODS:
      if user.groups.filter(name='administrator'):
        return True
    else:
      return False