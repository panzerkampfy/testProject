from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from trello2.tasks import send_verification_email, hello


class User(AbstractUser):
    city = models.CharField(max_length=100, null=True)
    is_verified = models.BooleanField('verified', default=False)


@receiver(post_save, sender=User)
def send_verified_mail(sender, instance: User, **kwargs):
    if not instance.is_verified and len(instance.password) > 0:
        send_verification_email.delay(instance.id)
