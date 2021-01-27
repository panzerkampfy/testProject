from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Task(models.Model):
    text = models.CharField(max_length=255)
    # column = models.ForeignKey("Column", on_delete=models.CASCADE, default=0)


class Column(models.Model):
    title_column = models.CharField(max_length=100)
    tasks = models.ManyToManyField("Task", through="TaskColumn")
    # board = models.ForeignKey("Board", on_delete=models.CASCADE, default=0)


class TaskColumn(models.Model):
    task = models.ForeignKey("Task", on_delete=models.CASCADE)
    column = models.ForeignKey("Column", on_delete=models.CASCADE)


class Board(models.Model):
    title_board = models.CharField(max_length=50)
    columns = models.ManyToManyField("Column", through="ColumnBoard")
    # users = models.ManyToManyField(User, through='PermissionOnBoard')


class ColumnBoard(models.Model):
    column = models.ForeignKey("Column", on_delete=models.CASCADE)
    board = models.ForeignKey("Board", on_delete=models.CASCADE)


class PermissionOnBoard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    board = models.ForeignKey("Board", on_delete=models.CASCADE)
    permission_types = (
        (1, 'Owner'),
        (2, 'Member'),
        (3, 'Visitor'),
        (4, 'Admin'),

    )
    permission = models.IntegerField(choices=permission_types)
