import factory

from table.models import User, Board, Column, Task, PermissionOnBoard


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User


class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board

    title_board = 'board 1'


class PermissionOnBoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PermissionOnBoard

    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)
    permission = '1'


class ColumnFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Column

    title_column = 'column 1'
    board = factory.SubFactory(BoardFactory)


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    text = 'text 1'
    column = factory.SubFactory(ColumnFactory)
