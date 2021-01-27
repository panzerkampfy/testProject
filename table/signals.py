from django.db.models.signals import post_delete
from django.dispatch import receiver

from table.models import Column


@receiver(post_delete, sender=Column)
def delete_tasks(sender, instance: Column, **kwargs):
    instance.tasks.delete()
