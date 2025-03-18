from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

class AuthenticationService(BaseBackend):
    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
    
    """
    Authenticate users using their email.
    """
    @staticmethod
    def authenticate(request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None

    @staticmethod
    def generate_tokens_for_user(user):
        """
        Generate JWT tokens for the given user and include custom claims.
        """
        refresh = RefreshToken.for_user(user)
    
        # Add custom claims to the token
        refresh['username'] = user.username
        refresh['email'] = user.email
        refresh['is_instructor'] = user.is_instructor
        refresh['is_student'] = user.is_student
        refresh['first_name'] = user.first_name
        refresh['last_name'] = user.last_name
        # Add any other user information you need
    
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }