from rest_framework import serializers
from ..models import CoursesLesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursesLesson
        fields = ['lessonId', 'title', 'description', 'courseId', 'video', 'created_at', 'updated_at']