from rest_framework import status 
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed 
from .config import VALID_URLS
from django.http import JsonResponse


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            self.auth_check(request)
        except AuthenticationFailed as e:
            return self.unauthorized_response(e)
        
        response = self.get_response(request)
        return response

    def auth_check(self, request):
        if (
            request.path not in VALID_URLS
            and ("Authorization" not in request.headers
            or not self.is_token_valid(request))
        ):
            print(f"Authorized Access! {self.is_token_valid(request)}")
            raise AuthenticationFailed("UnAuthorized Access!", code="unauthorized")
        
    def is_token_valid(self, request):
        JWTAuthenticator = JWTAuthentication()
        unValidated_token = request.headers["Authorization"].split(' ')[1] if "Authorization" in request.headers else None
        decoded_token = JWTAuthenticator.get_validated_token(unValidated_token)

        return decoded_token is not None
        
    def unauthorized_response(self, message):
        return JsonResponse({"error": str(message)}, status=status.HTTP_401_UNAUTHORIZED)
