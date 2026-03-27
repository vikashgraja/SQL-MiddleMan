import pytest
from rest_framework.test import APIClient
from django.conf import settings
import os

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def auth_client(api_client):
    """Client with a valid API-Key header."""
    key = getattr(settings, "API_KEY", os.environ.get("API_KEY", "testkey123"))
    api_client.credentials(HTTP_AUTHORIZATION=f"API-Key {key}")
    return api_client

@pytest.fixture
def x_api_key_client(api_client):
    """Client using the X-API-KEY header."""
    key = getattr(settings, "API_KEY", os.environ.get("API_KEY", "testkey123"))
    api_client.credentials(HTTP_X_API_KEY=key)
    return api_client
