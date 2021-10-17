import pytest

pytestmark = pytest.mark.django_db


class TestRegistration:
    @pytest.fixture(autouse=True)
    def setup(self, api_client, user1):
        self.api_client = api_client
        # self.api_client.force_authenticate(user1)
        self.user = user1

    def test_reg(self, user_data):
        response = self.api_client.post('/api/v1/registration/', data=user_data)
        assert response.status_code == 201

    def test_login(self):
        data = {
            "username": "username1",
            "password": "password1"
        }
        response = self.api_client.post('/api/v1/login/', data=data)
        assert response.status_code == 201
