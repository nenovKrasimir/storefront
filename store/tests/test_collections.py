from django.contrib.auth.models import User
from rest_framework import status

import pytest


@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/store/collections/')
    return do_create_collection


@pytest.mark.django_db
class TestCreateCollection:

    def test_if_user_is_anonymous_returns_401(self, create_collection):
        response = create_collection({'title': 'a'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_if_data_is_invalid_returns_400(self, authenticate, create_collection):
        authenticate(is_staff=False)

        response = create_collection({'title': 'a'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
    

    def test_if_data_is_valid_returns_201(self, api_client):
        
        api_client.force_authenticate(user=User(is_staff=True))
        response = api_client.post('/store/collections/', {'title': 'a'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0