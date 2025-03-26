from rest_framework import serializers
from ..models import User, UserCoursePurchase

class UserCoursePurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCoursePurchase
        fields = ['user', 'course', 'purchase_date']