from django.conf import settings
from rest_framework import generics
from ..serializers.users_serializers import LoginSerializer, UserSerializer
from ..models.user_model import User
from rest_framework.views import APIView
from rest_framework.response import Response
import logging
from ..services.auth_service import AuthenticationService
from django.contrib.auth import login, logout
from ..form_validations.user_creation_validation import CustomUserCreationForm
import json

logger = logging.getLogger(__name__)


class UserCreateView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        if request.method == 'POST':
            body = json.loads(request.body)
            form = CustomUserCreationForm(body)
            if form.is_valid():
                user = form.save()
                return Response({'success': True, 'user_id': user.id})
            else:
                return Response({
                    'success': False,
                    'errors': form.get_validation_errors()
                }, status=400)
        return Response({'error': 'Method not allowed'}, status=405)


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Email and password are required."}, status=400)

        # Authenticate the user using email and password
        user = AuthenticationService.authenticate(
            request=request, email=email, password=password
        )
        if user is None:
            return Response({"error": "Invalid email or password."}, status=400)

        # Generate tokens with custom claims
        tokens = AuthenticationService.generate_tokens_for_user(user)

        if tokens is None:
            return Response({"error": "UnAuthorized"}, status=401)

        login(request=request, user=user)

        response = Response(
            {
                "access_token": tokens["access"],
                "refresh_token": tokens["refresh"],
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "is_instructor": user.is_instructor,
                    "is_student": user.is_student,
                },
            },
            status=202,
        )

        response.set_cookie(
            key="token",  # Cookie name
            value=tokens["access"],  # Cookie value
            httponly=True,  # Prevent client-side JavaScript from accessing the cookie
            secure=settings.DEBUG is False,  # Send only over HTTPS in production
            samesite="lax",  # Prevent CSRF attacks
            max_age=86400,  # Cookie expiry time in seconds (1 day)
            path="/",  # Cookie accessible across the entire domain
        )

        return response


class LogoutView(APIView):
    def post(self, request):
        userToken = request.headers.get("authorization")
        if not userToken:
            return Response(
                {"error": "unAuthorized!"},
                status=401,
            )

        user = AuthenticationService.decode_jwt_token(userToken)

        request.user = user

        response = Response(
            {
                "user": {"username": user.get("username"), "message": "Logged out!"},
            },
            status=201,
        )

        response.set_cookie(
            key="token",  # Cookie name (must match the original cookie name)
            value="",  # Set the value to an empty string
            httponly=True,  # Must match the original cookie's HttpOnly flag
            secure=settings.DEBUG is False,  # Must match the original cookie's Secure flag
            samesite="lax",  # Must match the original cookie's SameSite attribute
            max_age=0,  # Set max_age to 0 to expire the cookie immediately
            path="/",  # Must match the original cookie's path
        )
        print(f"RESPONSE COOKIE==> {response.cookies}")

        logout(request=request)

        return response
