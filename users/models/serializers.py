from rest_framework import serializers
from django.contrib.auth.models import User
from .user_model import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'is_instructor', 'is_student']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            is_instructor=validated_data.get('is_instructor', False),
            is_student=validated_data.get('is_student', False),
        )
        return user