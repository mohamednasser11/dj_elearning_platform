from django.db import models
from django.core.validators import MinValueValidator


class InstructorModel(models.Model):
    user = models.OneToOneField(
        "User", on_delete=models.CASCADE, related_name="instructor_profile"
    )
    price_rate = models.DecimalField(
        default=0,
        max_digits=10,
        validators=[MinValueValidator(0)],
        decimal_places=2,
        verbose_name="Price Rate",
    )
    departments_taught = models.ManyToManyField(
        "departments.Departments",
        related_name="instructors",
        blank=True,
        verbose_name="Departments Taught",
    )

    def __str__(self):
        return f"{self.user.username} - Instructor"
