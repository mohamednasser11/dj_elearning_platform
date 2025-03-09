from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    id = models.AutoField(primary_key=True)  # Explicit id field
    is_instructor = models.BooleanField(default=False, verbose_name='Is Instructor')
    is_student = models.BooleanField(default=False, verbose_name='Is Student')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'