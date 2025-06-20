from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
import jwt
from decouple import config
import logging

logger = logging.getLogger(__name__)

class AuthenticationService(BaseBackend):
    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
    
    @staticmethod
    def authenticate(request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
            if user.check_password(password):
                return user
            logger.warning(f"Invalid password for user {email}")
        except UserModel.DoesNotExist:
            logger.warning(f"User with email {email} not found")
        return None

    @staticmethod
    def generate_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)
        
        # Add custom claims
        refresh['username'] = user.username
        refresh['email'] = user.email
        refresh['is_student'] = user.is_student
        refresh['first_name'] = user.first_name
        refresh['last_name'] = user.last_name
        
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

    @staticmethod
    def decode_jwt_token(token):
        [bearer, token] = token.split(' ')
        return jwt.decode(token, config("SIGNING_KEY"), ['HS256'])
    
    @staticmethod
    def validate_jwt_token(token):
        """
        Validates JWT token using SimpleJWT's built-in verification
        Returns (is_valid, decoded_payload)
        """
        try:
            # Remove 'Bearer ' prefix if present
            if token.startswith('Bearer '):
                token = token[7:]
                
            validated_token = AccessToken(token)
            return True, validated_token.payload
        except (InvalidToken, TokenError, jwt.PyJWTError) as e:
            logger.error(f"Token validation failed: {str(e)}")
            return False, None

    @staticmethod
    def get_user_from_token(token):
        """
        Extracts user from validated JWT token
        """
        is_valid, payload = AuthenticationService.validate_jwt_token(token)
        if not is_valid:
            return None
            
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(id=payload['user_id'])
        except (UserModel.DoesNotExist, KeyError):
            return None