from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from .config import VALID_URLS


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.auth_check(request)
        response = self.get_response(request)
        return response

    def auth_check(self, request):
        if (
            request.path not in VALID_URLS
            and "Authorization" not in request.headers
            and self.is_token_valid(request)
        ):
            return JsonResponse(
                {"error": "unAuthorized!"},
                status=401,
            )
        
    def is_token_valid(slef, request):
        JWTAuthenticator = JWTAuthentication()

        decoded_token = JWTAuthenticator.authenticate(request=request)

        if decoded_token is not None:
            return True
        else:
            return False
