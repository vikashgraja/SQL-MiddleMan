import pytest
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
def test_authentication_required(api_client):
    url = "/ingestion/sample_data/fetch/"
    response = api_client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_authentication_with_valid_key(auth_client):
    url = "/ingestion/sample_data/fetch/"
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_authentication_with_x_api_key(x_api_key_client):
    url = "/ingestion/sample_data/fetch/"
    response = x_api_key_client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_authentication_with_invalid_key(api_client):
    url = "/ingestion/sample_data/fetch/"
    api_client.credentials(HTTP_AUTHORIZATION="API-Key wrong-key")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
