from rest_framework import viewsets
from quotation.models import Demand
from quotation.serializers import DemandSerializer
from mytools.permissions import IsAdvertiser

class DemandViewSet(viewsets.ModelViewSet):
  """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
  """
  queryset = Demand.objects.all()
  serializer_class = DemandSerializer
  permission_classes = [IsAdvertiser]
