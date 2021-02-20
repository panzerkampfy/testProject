import pytest
from table.models import User, PermissionOnBoard

pytestmark = pytest.mark.django_db


class TestBoardView:
    @pytest.fixture(autouse=True)
    def setup(self, api_client):
        self.api_client = api_client
        user = User.objects.create(username='username', password='password', email="jk@mail.com")
        self.api_client.force_authenticate(user)

    def create_board(self, data):
        response = self.api_client.post('/api/v1/boards/', data=data)
        return response

    def test_create_board(self, new_board_data):
        response = self.create_board(data=new_board_data)
        assert response.status_code == 201

    def test_create_board_not_valid(self, new_board_data_not_valid):
        response = self.create_board(data=new_board_data_not_valid)
        assert response.status_code == 400

    def test_update_board(self, new_board_data, update_board_data, update_board_data_not_valid):
        response = self.create_board(data=new_board_data)
        assert response.status_code == 201

        board_id = str(response.data['id'])
        path = '/api/v1/boards/' + board_id + '/'
        response = self.api_client.put(path, data=update_board_data)
        assert response.status_code == 202

        response = self.api_client.put(path, data=update_board_data_not_valid)
        assert response.status_code == 400

    def test_delete_board(self, new_board_data):
        response = self.create_board(data=new_board_data)
        assert response.status_code == 201

        board_id = str(response.data['id'])
        path = '/api/v1/boards/' + board_id + '/'
        response = self.api_client.delete(path)
        assert response.status_code == 204


class TestColumnView:
    @pytest.fixture(autouse=True)
    def setup(self, api_client):
        self.api_client = api_client
        user = User.objects.create(username='username', password='password', email="jk@mail.com")
        self.api_client.force_authenticate(user)

    def create_column(self, data):
        path = '/api/v1/column/'
        response = self.api_client.post(path, data=data, format='json')
        return response

    def test_create_column(self, new_board_data):
        response = TestBoardView.create_board(self=self, data=new_board_data)
        assert response.status_code == 201

        board_id = str(response.data['id'])
        new_column_data = {"board": board_id, "title_column": "column 1"}
        response = self.create_column(data=new_column_data)
        assert response.status_code == 201

        new_column_data_not_valid = {"board": "", "title_column": "column 1"}
        response = self.create_column(data=new_column_data_not_valid)
        assert response.status_code == 400

    def test_update_column(self, update_column_data, new_board_data, update_column_data_not_valid):
        response = TestBoardView.create_board(self=self, data=new_board_data)
        assert response.status_code == 201

        board_id = str(response.data['id'])
        new_column_data = {"board": board_id, "title_column": "column 1"}
        response = self.create_column(data=new_column_data)
        assert response.status_code == 201

        column_id = str(response.data['id'])
        path = '/api/v1/columns/' + column_id + '/'
        response = self.api_client.put(path, data=update_column_data)
        assert response.status_code == 202

        response = self.api_client.put(path, data=update_column_data_not_valid)
        assert response.status_code == 400

    #
    def test_delete_column(self, new_board_data):
        response = TestBoardView.create_board(self=self, data=new_board_data)
        assert response.status_code == 201

        board_id = str(response.data['id'])
        new_column_data = {"board": board_id, "title_column": "column 1"}
        response = self.create_column(data=new_column_data)
        assert response.status_code == 201

        column_id = str(response.data['id'])
        path = '/api/v1/columns/' + column_id + '/'
        response = self.api_client.delete(path)
        assert response.status_code == 204


class TestTaskView:
    @pytest.fixture(autouse=True)
    def setup(self, api_client):
        self.api_client = api_client
        user = User.objects.create(username='username', password='password', email="jk@mail.com")
        self.api_client.force_authenticate(user)

    def create_task(self, data):
        path = '/api/v1/task/'
        response = self.api_client.post(path, data=data, format='json')
        return response

    def test_create_task(self, new_board_data):
        response = TestBoardView.create_board(self=self, data=new_board_data)
        assert response.status_code == 201

        board_id = str(response.data['id'])
        new_column_data = {"board": board_id, "title_column": "column 1"}
        response = TestColumnView.create_column(self=self, data=new_column_data)
        assert response.status_code == 201

        column_id = str(response.data['id'])
        new_task_data = {"column": column_id, "text": "sdffsdff3"}
        response = self.create_task(data=new_task_data)
        assert response.status_code == 201

        new_task_data = {"column": "2", "text": "sdffsdff3"}
        response = self.create_task(data=new_task_data)
        assert response.status_code == 400

    def test_update_task(self, new_board_data, update_task_data, update_task_data_not_valid):
        response = TestBoardView.create_board(self=self, data=new_board_data)
        assert response.status_code == 201

        board_id = str(response.data['id'])
        new_column_data = {"board": board_id, "title_column": "column 1"}
        response = TestColumnView.create_column(self=self, data=new_column_data)
        assert response.status_code == 201

        column_id = str(response.data['id'])
        new_task_data = {"column": column_id, "text": "sdffsdff3"}
        response = self.create_task(data=new_task_data)
        assert response.status_code == 201

        task_id = str(response.data['id'])
        path = '/api/v1/tasks/' + task_id + '/'
        response = self.api_client.put(path, data=update_task_data, format='json')
        assert response.status_code == 202

        response = self.api_client.put(path, data=update_task_data_not_valid, format='json')
        assert response.status_code == 400

        # move to 2nd column
        new_column_data = {"board": board_id, "title_column": "column 2"}
        response = TestColumnView.create_column(self=self, data=new_column_data)
        assert response.status_code == 201

        column_id = str(response.data['id'])
        path = '/api/v1/tasks/' + task_id + '/'
        update_task_data = {"column": column_id}
        response = self.api_client.put(path, data=update_task_data, format='json')
        assert response.status_code == 202

    def test_delete_task(self, new_board_data):
        response = TestBoardView.create_board(self=self, data=new_board_data)
        assert response.status_code == 201

        board_id = str(response.data['id'])
        new_column_data = {"board": board_id, "title_column": "column 1"}
        response = TestColumnView.create_column(self=self, data=new_column_data)
        assert response.status_code == 201

        column_id = str(response.data['id'])
        new_task_data = {"column": column_id, "text": "sdffsdff3"}
        response = self.create_task(data=new_task_data)
        assert response.status_code == 201

        task_id = str(response.data['id'])
        path = '/api/v1/tasks/' + task_id + '/'
        response = self.api_client.delete(path)
        assert response.status_code == 204


class TestPermissions:
    @pytest.fixture(autouse=True)
    def setup(self, api_client):
        self.api_client = api_client
        self.user1 = User.objects.create(username='username1', password='password1', email="j1k@mail.com")
        self.api_client.force_authenticate(self.user1)

        self.user2 = User.objects.create(username='username2', password='password2', email="j2k@mail.com")

    def test_create_permission(self, new_board_data):
        response = TestBoardView.create_board(self, new_board_data)
        assert response.status_code == 201

        board_id = str(response.data['id'])
        user_id = self.user1.id
        obj = PermissionOnBoard.objects.get(user=user_id, board=board_id)
        assert obj.permission == 1

        self.api_client.force_authenticate(self.user2)
        user2_id = self.user2.id
        data = {"user": user2_id, "board": board_id, "permission": 2}
        path = '/api/v1/permissions/'
        response = self.api_client.put(path, data=data)
        assert response.status_code == 403

        self.api_client.force_authenticate(self.user1)
        response = self.api_client.put(path, data=data)
        assert response.status_code == 201
