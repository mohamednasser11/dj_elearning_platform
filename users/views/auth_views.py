from django.conf import settings
from rest_framework import status
from ..serializers.users_serializers import LoginSerializer, UserSerializer
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
        if request.method == "POST":
            body = json.loads(request.body)
            form = CustomUserCreationForm(body)
            if form.is_valid():
                user = form.save()
                return Response({"success": True, "user_id": user.id})
            else:
                return Response(
                    {"success": False, "errors": form.get_validation_errors()},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        try:
            # Manually parse the body if request.data fails
            raw_data = json.loads(
                request.body.decode("utf-8")
            )  # Manually decode and parse JSON
        except json.JSONDecodeError as e:
            logger.error(f"JSON Decode Error: {str(e)}")
            return Response({"error": "Invalid JSON format."}, status=status.HTTP_400_BAD_REQUEST)

        email = raw_data.get("email")
        password = raw_data.get("password")
        if not email or not password:
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate the user using email and password
        user = AuthenticationService.authenticate(
            request=request, email=email, password=password
        )
        if user is None:
            return Response({"error": "Invalid email or password."}, status=status.HTTP_400_BAD_REQUEST)

        # Generate tokens with custom claims
        tokens = AuthenticationService.generate_tokens_for_user(user)

        if tokens is None:
            return Response({"error": "UnAuthorized"}, status=status.HTTP_401_UNAUTHORIZED)

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
        userToken = request.headers.get("Authorization")
        if not userToken:
            return Response(
                {"error": "unAuthorized!"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user = AuthenticationService.decode_jwt_token(userToken)

        request.user = user

        response = Response(
            {
                "user": {"username": user.get("username"), "message": "Logged out!"},
            },
            status=status.HTTP_200_OK,
        )

        response.set_cookie(
            key="token",  # Cookie name (must match the original cookie name)
            value="",  # Set the value to an empty string
            httponly=True,  # Must match the original cookie's HttpOnly flag
            secure=settings.DEBUG
            is False,  # Must match the original cookie's Secure flag
            samesite="lax",  # Must match the original cookie's SameSite attribute
            max_age=0,  # Set max_age to 0 to expire the cookie immediately
            path="/",  # Must match the original cookie's path
        )

        logout(request=request)

        return response
