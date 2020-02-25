from rest_framework import viewsets
# Permissions
from mytools.permissions import IsAdvertiser
# Models
from quotation.models import Demand
# Serializers
from quotation.serializers import DemandSerializer

class DemandViewSet(viewsets.ModelViewSet):
  """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
  """
  serializer_class = DemandSerializer
  permission_classes = [IsAdvertiser]
  def get_queryset(self):
    if(self.request.user.groups.filter(name='administrator')):
      return Demand.objects.all()
    else:
      return Demand.objects.filter(owner_id=self.request.user.id)
