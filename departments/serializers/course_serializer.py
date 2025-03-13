from rest_framework import serializers
from ..models.course_models import Course
from ..models.departments_models import Departments

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model= Course
        fields= ('courseId', 'title', 'description', 'price', 'departmentId', 'instructorId', 'created_at', 'updated_at')
        

