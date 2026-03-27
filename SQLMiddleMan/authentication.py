import os
import secrets
import logging

from django.conf import settings
from rest_framework import authentication
from rest_framework import exceptions
from django.contrib.auth.models import AnonymousUser

class APIKeyUser(AnonymousUser):
    @property
    def is_authenticated(self):
        return True

class APIKeyAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Allow passing the key in the Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        api_key = None

        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() in ('api-key', 'token', 'bearer'):
                api_key = parts[1]
            elif len(parts) == 1:
                api_key = parts[0]
        
        # Alternative: allow passing in X-API-KEY header
        if not api_key:
            api_key = request.META.get('HTTP_X_API_KEY')

        if not api_key:
            return None

        # Check against the environment variable API_KEY
        expected_key = getattr(settings, "API_KEY", os.environ.get("API_KEY"))
        
        if not expected_key:
            raise exceptions.AuthenticationFailed("API Key is not configured on the server.")

        # Constant-time comparison to prevent timing attacks
        if secrets.compare_digest(api_key, expected_key):
            return (APIKeyUser(), None)

        logger = logging.getLogger(__name__)
        logger.warning(f"Failed authentication attempt from {request.META.get('REMOTE_ADDR')}")
        raise exceptions.AuthenticationFailed('Invalid API Key')
