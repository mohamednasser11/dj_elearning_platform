from rest_framework import serializers
from ..models.courses_models.course_models import Course

class CoureseOfDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'department', 'created_at', 'updated_at']