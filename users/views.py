from rest_framework import generics
from .models.serializers import UserSerializer
from .models.user_model import User

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer