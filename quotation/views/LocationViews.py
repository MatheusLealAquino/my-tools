from rest_framework import viewsets
# Permissions
from rest_framework.permissions import IsAuthenticated
# Models
from quotation.models import City, State
# Serializers
from quotation.serializers import CitySerializer, StateSerializer


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