from django.db import models
from django.core.validators import RegexValidator
from mytools.models import OwnedModel

class State(models.Model):
  name = models.CharField(max_length=2, blank=False, unique=True)

  def __str__(self):
    return self.name

class City(models.Model):
  name = models.CharField(max_length=50, blank=False, unique=True)
  state = models.ForeignKey(State, on_delete=models.CASCADE)

  def __str__(self):
    return self.name + ' - ' + self.state.name

class Demand(OwnedModel):
  created = models.DateTimeField(auto_now_add=True)
  description = models.TextField(blank=False)
  street_name = models.TextField(blank=False)
  number_address = models.DecimalField(default=0, max_digits=10, decimal_places=0)
  city = models.ForeignKey(City, on_delete=models.CASCADE)
  cep = models.CharField(
    max_length=20,
    blank=False,
    validators=[
      RegexValidator(
        regex='([0-9]{5}-[\d]{3})'
      )
    ]
  )
  email = models.EmailField(default='')
  cellphone = models.CharField(
    max_length=50,
    blank=False,
    validators=[
      RegexValidator(
        regex='(\(?\d{2}\)?\s)?(\d{4,5}\-?\d{4})'
      )
    ]
  )
  status = models.BooleanField(default=False)
