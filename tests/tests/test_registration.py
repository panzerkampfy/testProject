import pytest

pytestmark = pytest.mark.django_db


class TestRegistration:
    @pytest.fixture(autouse=True)
    def setup(self, api_client):
        self.api_client = api_client

    def test_reg(self, user_data):
        response = self.api_client.post('/api/v1/registration/', data=user_data)
        assert response.status_code == 201
