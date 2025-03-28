from rest_framework import serializers
from ..models.departments_models import Departments

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model= Departments
        fields= ['departmentId', 'name']