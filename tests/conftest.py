import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


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
