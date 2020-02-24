from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
# Permissions
from mytools.permissions import IsAdvertiser
from rest_framework.permissions import IsAuthenticated
# Models
from quotation.models import Demand, City, State
from django.contrib.auth.models import User, Group
# Serializers
from quotation.serializers import DemandSerializer, UserSerializer, GroupSerializer, CitySerializer, StateSerializer

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

class CityViewSet(viewsets.ReadOnlyModelViewSet):
  """
    API endpoint that allows cities to be viewed or edited.
  """
  queryset = City.objects.all()
  serializer_class = CitySerializer
  permission_classes = [IsAuthenticated]

class StateViewSet(viewsets.ReadOnlyModelViewSet):
  """
    API endpoint that allows states to be viewed or edited.
  """
  queryset = State.objects.all()
  serializer_class = StateSerializer
  permission_classes = [IsAuthenticated]

class UserGroupViewSet(viewsets.ViewSet):
  permission_classes = [IsAuthenticated]

  """
    API endpoint that allows assign a user to group
  """
  def create(self, request):
    if not request.user.is_superuser:
      if request.user.id is not request.data['user_id']:
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
        'message': "Can't find group"
      }, status=status.HTTP_400_BAD_REQUEST)
    
    if group.name == 'administrator':
      if not request.user.is_superuser:
        return Response({
          'message': "Not authorized to associate to this group"
        }, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.get(id=request.data['user_id'])
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
      return Response(response, status=status.HTTP_201_CREATED)
    except:
      return Response({
        'message': "Can't associate user to the group"
      }, status=status.HTTP_400_BAD_REQUEST)

class DemandViewSet(viewsets.ModelViewSet):
  """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
  """
  serializer_class = DemandSerializer
  permission_classes = [IsAdvertiser]
  def get_queryset(self):
    return Demand.objects.filter(owner_id=self.request.user.id)
