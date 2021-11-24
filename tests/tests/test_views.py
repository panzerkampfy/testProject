import pytest

pytestmark = pytest.mark.django_db


class BaseTestClass:
    @pytest.fixture(autouse=True)
    def setup(self, api_client, user1):
        self.api_client = api_client
        self.api_client.force_authenticate(user1)


class TestBoardView(BaseTestClass):
    def test_create_board(self, new_board_data):
        response = self.api_client.post('/api/v1/boards/', data=new_board_data)
        assert response.status_code == 201

    def test_create_board_not_valid(self, new_board_data_not_valid):
        response = self.api_client.post('/api/v1/boards/', data=new_board_data_not_valid)
        assert response.status_code == 400

    def test_update_board(self, update_board_data, update_board_data_not_valid, board):
        board_id = str(board.id)
        path = '/api/v1/boards/' + board_id + '/'
        response = self.api_client.put(path, data=update_board_data)
        assert response.status_code == 202

        response = self.api_client.put(path, data=update_board_data_not_valid)
        assert response.status_code == 400

    def test_delete_board(self, board):
        board_id = str(board.id)
        path = '/api/v1/boards/' + board_id + '/'
        response = self.api_client.delete(path)
        assert response.status_code == 204


class TestColumnView(BaseTestClass):
    def test_create_column(self, board):
        board_id = str(board.id)
        new_column_data = {"board": board_id, "title_column": "column 1"}
        response = self.api_client.post('/api/v1/columns/', data=new_column_data, format='json')
        assert response.status_code == 201

        new_column_data_not_valid = {"board": "", "title_column": "column 1"}
        response = self.api_client.post('/api/v1/columns/', data=new_column_data_not_valid, format='json')
        assert response.status_code == 400

    def test_update_column(self, column, update_column_data, update_column_data_not_valid):
        column_id = str(column.id)
        path = '/api/v1/columns/' + column_id + '/'
        response = self.api_client.put(path, data=update_column_data)
        assert response.status_code == 202

        response = self.api_client.put(path, data=update_column_data_not_valid)
        assert response.status_code == 400

    def test_delete_column(self, column):
        column_id = str(column.id)
        path = '/api/v1/columns/' + column_id + '/'
        response = self.api_client.delete(path)
        assert response.status_code == 204


class TestTaskView(BaseTestClass):
    def test_create_task(self, column):
        column_id = str(column.id)
        new_task_data = {"column": column_id, "text": "sdffsdff3"}
        response = self.api_client.post('/api/v1/tasks/', data=new_task_data, format='json')
        assert response.status_code == 201

        new_task_data = {"column": "", "text": "sdffsdff3"}
        response = self.api_client.post('/api/v1/tasks/', data=new_task_data, format='json')
        assert response.status_code == 400

    def test_update_task(self, task, update_task_data, update_task_data_not_valid):
        task_id = str(task.id)
        path = '/api/v1/tasks/' + task_id + '/'
        response = self.api_client.put(path, data=update_task_data, format='json')
        assert response.status_code == 202

        response = self.api_client.put(path, data=update_task_data_not_valid, format='json')
        assert response.status_code == 400

    def test_delete_task(self, task):
        task_id = str(task.id)
        path = '/api/v1/tasks/' + task_id + '/'
        response = self.api_client.delete(path)
        assert response.status_code == 204


class TestPermissions(BaseTestClass):
    def test_permission(self, user2, new_board_data, update_board_data):
        response = self.api_client.post('/api/v1/boards/', data=new_board_data)
        board_id = str(response.data.get('id'))
        print(response.data)
        self.api_client.force_authenticate(user2)
        data = {"user": user2.id, "board": board_id, "permission": 2}
        response = self.api_client.put('/api/v1/permissions/', data=data)
        print(response.data)
        assert response.status_code == 403

        path = '/api/v1/boards/' + board_id + '/'
        response = self.api_client.put(path, data=update_board_data)
        print(response.data)
        assert response.status_code == 403
