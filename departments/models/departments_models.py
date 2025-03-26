from django.db import models


class Departments(models.Model):
    departmentId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name='Departement Name')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
