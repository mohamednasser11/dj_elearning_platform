from django.db import models
from django.core.validators import MinValueValidator


# Create your models here.
class Courses(models.Model):
    courseId = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name="Course Title")
    description = models.CharField(max_length=500, verbose_name="Course Description")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    departmentId = models.ForeignKey(
        "Department",
        on_delete=models.CASCADE,
        related_name="courses",
        verbose_name="Department",
    )
    instructorId = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="courses_taught",
        verbose_name="Instructor",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Created At")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ["title"]


class Department(models.Model):
    departementId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name='Departement Name')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

