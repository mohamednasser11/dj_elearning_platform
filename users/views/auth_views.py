from django.conf import settings
from rest_framework import generics
from ..serializers.users_serializers import LoginSerializer, UserSerializer
from ..models.user_model import User
from rest_framework.views import APIView
from rest_framework.response import Response
import logging
from ..services.auth_service import AuthenticationService

logger = logging.getLogger(__name__)


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginView(APIView):
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
