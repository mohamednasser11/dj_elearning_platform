from django.http import JsonResponse


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.auth_check(request)
        response = self.get_response(request)
        return response

    def auth_check(self, request):

        if (
            (request.path != "/api/v1/users/login/" or request.path != "/api/v1/users/register/")
            and "Authorization" not in request.headers
        ):
            return JsonResponse(
                {"error": "unAuthorized!"},
                status=401,
            )
