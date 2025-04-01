from django.http import JsonResponse
from rest_framework import status 
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed 
from .config import VALID_URLS


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
            print(f"Method ==> {request.path}")
            raise AuthenticationFailed("UnAuthorized Access!", code="unauthorized")
        
    def is_token_valid(self, request):
        JWTAuthenticator = JWTAuthentication()
        [bearer, unValidated_token] = request.headers["Authorization"].split(' ') if "Authorization" in request.headers else None
        print(f"Unvalidated Token: {unValidated_token}")
        decoded_token = JWTAuthenticator.get_validated_token(unValidated_token)
        print(f"decoded_token: {decoded_token}")

        return decoded_token is not None
        
    def unauthorized_response(self, message):
        return JsonResponse({"error": str(message)}, status=status.HTTP_401_UNAUTHORIZED)
