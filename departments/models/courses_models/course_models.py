from django.db import models
from django.core.validators import MinValueValidator


# Create your models here.
class Course(models.Model):
    courseId = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name="Course Title")
    description = models.CharField(max_length=500, verbose_name="Course Description")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    departmentId = models.ForeignKey(
        "Departments",
        on_delete=models.CASCADE,
        related_name="course",
        verbose_name="Department",
    )
    instructorId = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="courses_taught",
        verbose_name="Instructor",
    )
    rating = models.DecimalField(default=0, max_digits=3, decimal_places=1)
    field = models.CharField(
        max_length=100,
        verbose_name="Course Field",
        blank=True,
        null=True
    )
    number_of_students = models.PositiveIntegerField(default=0)
    image_url = models.FileField(upload_to="courses/thumbnails/")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ["created_at"]
