from mytools.serializers import DynamicFieldsModelSerializer
from quotation.models import Demand
from rest_framework import serializers

class DemandSerializer(DynamicFieldsModelSerializer):
  class Meta:
    model = Demand
    fields = ['description', 'street_name', 'number_address', 'city', 'email', 'cellphone', 'status']
