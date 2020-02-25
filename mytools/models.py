from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class OwnedModel(models.Model):
  owner = models.ForeignKey(
    User,
    on_delete=models.CASCADE
  )

  def __str__(self):
    return self.owner.first_name + '  ' + self.owner.last_name

  class Meta:
    abstract = True