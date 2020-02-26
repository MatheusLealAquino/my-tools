from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
# Permissions
from rest_framework.permissions import IsAuthenticated
# Models
from django.contrib.auth.models import User, Group
# Serializers
from quotation.serializers import UserSerializer, GroupSerializer

class UserViewSet(viewsets.ViewSet):
  """
    API endpoint for user activities
  """
  def create(self, request):
    serialized = UserSerializer(data=request.data, context={'request': request})
    if(serialized.is_valid()):
      User.objects.create_user(
        username=serialized.validated_data['username'],
        email=serialized.validated_data['email'],
        password=serialized.validated_data['password'],
        first_name=serialized.validated_data['first_name'],
        last_name=serialized.validated_data['last_name'],
        is_active=True
      )
      user = User.objects.get(username=serialized.data['username'])
      response = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
      }
      return Response(response, status=status.HTTP_201_CREATED)
    else:
      return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

class GroupViewSet(viewsets.ReadOnlyModelViewSet):
  """
    API endpoint that allows groups to be viewed or edited.
  """
  queryset = Group.objects.all()
  serializer_class = GroupSerializer
  permission_classes = [IsAuthenticated]

class UserGroupViewSet(viewsets.ViewSet):
  permission_classes = [IsAuthenticated]

  """
    API endpoint that allows assign a user to group
  """
  def create(self, request, pk=None):
    if pk is None:
      return Response({
        'message': "Can't find the user identification"
      }, status=status.HTTP_400_BAD_REQUEST)

    '''
      Validade if is possible associate the user with the group.
      Only superuser can add another users beyond them self.
    '''
    if not request.user.is_superuser:
      if not str(request.user.id) == str(pk):
        return Response({
          'message': "Can't assign to that user, with this level of authentication"
        }, status=status.HTTP_400_BAD_REQUEST)

    # Verify the variable where contains identification of the group
    if 'group_id' in request.data:
      group = Group.objects.get(id=request.data['group_id'])
    elif 'group_name' in request.data:
      group = Group.objects.get(name=request.data['group_name'])
    else:
      return Response({
        'message': "Can't find the group identification"
      }, status=status.HTTP_400_BAD_REQUEST)
    
    if group.name == 'administrator':
      if not request.user.is_superuser:
        return Response({
          'message': "Not authorized to associate to this group"
        }, status=status.HTTP_400_BAD_REQUEST)

    # Get the user from the pk
    user = User.objects.get(id=pk)

    # Verify if user is already in one group
    if user.groups.filter(name='administrator') and group.name == 'advertiser':
      return Response({
        'message': "Can't associate user to advertiser group, because the user is already on administrator group"
      }, status=status.HTTP_400_BAD_REQUEST)
    elif user.groups.filter(name='advertiser') and group.name == 'administrator':
      return Response({
        'message': "Can't associate user to administrator group, because the user is already on advertiser group"
      }, status=status.HTTP_400_BAD_REQUEST)

    try:
      user.groups.add(group)
      response = {
        'user_id': user.id,
        'username': user.username,
        'group': {
          'id': group.id,
          'name': group.name
        }
      }

      # If the user is assigned to administrator group, give to him access on Django Admin
      if group.name == 'administrator':
        user.is_staff = True
        user.save()

      return Response(response, status=status.HTTP_201_CREATED)
    except:
      return Response({
        'message': "Can't associate user to the group (" + group.name + ")"
      }, status=status.HTTP_400_BAD_REQUEST)