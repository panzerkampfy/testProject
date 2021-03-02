from django.contrib.auth.models import User, AbstractUser
from django.db import models


class User(AbstractUser):
    city = models.CharField(max_length=100, null=True)
