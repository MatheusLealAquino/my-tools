from rest_framework import serializers
from mytools.serializers import DynamicFieldsModelSerializer
from quotation.models import Demand, City, State
from django.contrib.auth.models import User, Group

class DemandSerializer(DynamicFieldsModelSerializer):
  owner_id = serializers.HiddenField(
    default=serializers.CurrentUserDefault()
  )

  class Meta:
    model = Demand
    fields = ['id', 'description', 'street_name', 'number_address', 'city', 'email', 'cellphone', 'status', 'owner_id']

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password']
    extra_kwargs = {
      'password': {'write_only': True}
    }

class GroupSerializer(serializers.ModelSerializer):
  class Meta:
    model = Group
    fields = ['id', 'name']

class CitySerializer(serializers.ModelSerializer):
  class Meta:
    model = City
    fields = ['id', 'name', 'state_id']

class StateSerializer(serializers.ModelSerializer):
  class Meta:
    model = State
    fields = ['id', 'name']