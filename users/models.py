import uuid

from django.db import models
from django.contrib.auth.models import User


class Activation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
