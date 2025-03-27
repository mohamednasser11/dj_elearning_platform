from django.db import models

class CoursesOfDepartment(models.Model):
    department = models.ForeignKey('Departments', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)