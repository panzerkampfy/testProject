import pytest
from rest_framework.test import APIClient

from tests.factories.factories import *


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def user1() -> User:
    return UserFactory(username='username1', password='password1', email="j1k@mail.com")


@pytest.fixture
def user2() -> User:
    return UserFactory(username='username2', password='password2', email="j2k@mail.com")


@pytest.fixture
def board(user1) -> Board:
    board_object = BoardFactory(title_board='board 1')
    PermissionOnBoardFactory(user=user1, board=board_object, permission=1)
    return board_object


@pytest.fixture
def column(board) -> Column:
    return ColumnFactory(board=board, title_column='column 1')


@pytest.fixture
def task(column) -> Task:
    return TaskFactory(column=column)


@pytest.fixture
def user_data() -> {}:
    return {"username": "tests", "email": "testmail@mail.com",
            "password1": "any_strong_pass1",
            "password2": "any_strong_pass1",
            "city": "Tomsk"}


@pytest.fixture
def new_board_data() -> {}:
    return {"title_board": "board qwerty"}


@pytest.fixture
def new_board_data_not_valid() -> {}:
    return {"text_board": "board qwerty"}


@pytest.fixture
def update_board_data() -> {}:
    return {"title_board": "board qwert22y"}


@pytest.fixture
def update_board_data_not_valid() -> {}:
    return {"title": "column 1"}


@pytest.fixture
def new_column_data() -> {}:
    return {"title_column": "column 1"}


@pytest.fixture
def new_column_data_not_valid() -> {}:
    return {"title_board": "board qwerty"}


@pytest.fixture
def update_column_data() -> {}:
    return {"title_column": "column qwerty2"}


@pytest.fixture
def update_column_data_not_valid() -> {}:
    return {"title": "column 1"}


@pytest.fixture
def update_task_data() -> {}:
    return {"text": "sdf33"}


@pytest.fixture
def update_task_data_not_valid() -> {}:
    return {"tex": "sdf33"}
