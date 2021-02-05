from django.db.models.signals import post_delete
from django.dispatch import receiver

from table.models import Column, Task, Board


@receiver(post_delete, sender=Column)
def delete_tasks(sender, instance: Column, **kwargs):
    objs = Task.objects.filter(column=instance)
    for obj in objs:
        task = Task.objects.get(id=obj.task.id)
        task.delete()

@receiver(post_delete, sender=Board)
def delete_columns(sender, instance: Board, **kwargs):
    objs = Column.objects.filter(board=instance)
    for obj in objs:
        task = Column.objects.get(id=obj.task.id)
        task.delete()
