from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.http import JsonResponse
from rest_framework import status
from .config import VALID_PARENT_URLS, VALID_URLS


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            self.perform_authentication_if_needed(request)
        except AuthenticationFailed as e:
            return self.unauthorized_response(str(e))

        return self.get_response(request)

    def perform_authentication_if_needed(self, request):
        """Checks if authentication is required for this path, and processes it."""
        if not self.is_public_path(request.path):
            token = self.extract_token_from_header(request)
            self.authenticate_request(request, token)

    def is_public_path(self, path):
        """Returns True if the path is in the list of allowed public URLs."""
        normalized_path = path.rstrip("/")
        public_paths = [url.rstrip("/") for url in VALID_URLS]
        public_parent_paths = [url.rstrip("/") for url in VALID_PARENT_URLS]
        return normalized_path in public_paths or any(
            [normalized_path.startswith(parent) for parent in public_parent_paths]
        )

    def extract_token_from_header(self, request):
        """Extracts and returns the JWT token from the Authorization header."""
        auth_header = request.headers.get("Authorization", "")
        parts = auth_header.split()

        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise AuthenticationFailed("Invalid Authorization header format")

        return parts[1]

    def authenticate_request(self, request, token):
        """Validates the JWT and attaches the authenticated user to the request."""
        jwt_auth = JWTAuthentication()

        try:
            validated_token = jwt_auth.get_validated_token(token)
            request.user = jwt_auth.get_user(validated_token)
        except Exception as e:
            raise AuthenticationFailed(f"Token Error: {str(e)}")

    def unauthorized_response(self, message):
        """Returns a JSON response for unauthorized access."""
        return JsonResponse({"error": message}, status=status.HTTP_401_UNAUTHORIZED)
