from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    # username = models.CharField(max_length=30, unique=True)
    # city = models.CharField(max_length=100, null=True)
    pass
