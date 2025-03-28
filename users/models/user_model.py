from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    id = models.AutoField(primary_key=True)  # Explicit id field
    first_name = models.CharField(max_length=128, blank=True, null=True, verbose_name='First Name')
    last_name = models.CharField(max_length=128, blank=True, null=True, verbose_name= 'Last Name')
    email = models.EmailField(unique=True, verbose_name='Email Address')
    is_instructor = models.BooleanField(default=False, verbose_name='Is Instructor')
    is_student = models.BooleanField(default=False, verbose_name='Is Student')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    courses = models.ManyToManyField(
        'departments.Course',
        through='departments.UserCoursePurchase',  # <-- Key change: Use 'app_name.ModelName'
        related_name='enrolled_users',
        blank=True,
        verbose_name='Purchased Courses'
    )
    departments_taught = models.ManyToManyField(
        'departments.Departments',  # Reference to Department model
        related_name='instructors',
        blank=True,
        verbose_name='Departments Taught'
    )

    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Balance')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'