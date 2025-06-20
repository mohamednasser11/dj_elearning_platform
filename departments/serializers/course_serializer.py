from rest_framework import serializers
from ..models.courses_models.course_models import Course
from ..models.departments_models import Departments

class CourseSerializer(serializers.ModelSerializer):
    instructorId = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model= Course
        fields= ['courseId', 'title', 'description', 'price', 'departmentId', 'instructorId', 'image_url', 'rating', 'number_of_students', 'field', 'created_at', 'updated_at']
    
    def get_courses_count():
        return Course.objects.count()
    
    def get_all_coruses_fields():
        return set(Course.objects.values_list('field', flat=True).distinct())

