from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class OwnedModel(models.Model):
  owner = models.ForeignKey(
    User,
    on_delete=models.CASCADE
  )

  class Meta:
    abstract = True