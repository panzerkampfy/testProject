from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Task(models.Model):
    text = models.CharField(max_length=255)
    column = models.ForeignKey("Column", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, null=True)
    fact = models.CharField(max_length=511, null=True)
    weather = models.FloatField(null=True, blank=True)


class Column(models.Model):
    title_column = models.CharField(max_length=100)
    board = models.ForeignKey("Board", on_delete=models.CASCADE)


class Board(models.Model):
    title_board = models.CharField(max_length=50)
    users = models.ManyToManyField(User, through='PermissionOnBoard')


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
