from rest_framework import serializers
from users.models import Instructor
from users.models import User

class InstructorSerializer(serializers.ModelSerializer):
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Instructor
        fields = ['id', 'price_rate', 'user_details']

    def get_user_details(self, obj):
        user = User.objects.get(id=obj.user_id)
        return {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
    
    def create(self, validated_data):
        return super().create(validated_data)