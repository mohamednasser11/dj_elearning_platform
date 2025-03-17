from django.conf import settings
from rest_framework import generics
from ..serializers.users_serializers import LoginSerializer, UserSerializer
from ..models.user_model import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
import logging
import datetime

logger = logging.getLogger(__name__)


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = Response(
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "is_instructor": user.is_instructor,
                    "is_student": user.is_student,
                },
            }
        )

        response.set_cookie(
            key="token",  # Cookie name
            value=access_token,  # Cookie value
            httponly=True,  # Prevent client-side JavaScript from accessing the cookie
            secure=settings.DEBUG is False,  # Send only over HTTPS in production
            samesite='lax',  # Prevent CSRF attacks
            max_age=86400,  # Cookie expiry time in seconds (1 day)
            path="/",  # Cookie accessible across the entire domain
            )

        return response