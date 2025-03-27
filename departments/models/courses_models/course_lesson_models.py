from django.db import models
from .course_models import Course

class CoursesLesson(models.Model):
    courseId = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    video = models.FileField(upload_to='courses_lessons/videos/', blank=False)
    duration = models.DurationField() 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Course Lesson'
        verbose_name_plural = 'Course Lessons'
        ordering = ['created_at']