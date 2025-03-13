from rest_framework import generics
from departments.models.departments_models import Departments
from ..serializers.departments_serializer import DepartmentSerializer


class CreateDepartments(generics.ListCreateAPIView):
    queryset = Departments.objects.all()
    serializer_class = DepartmentSerializer


class UpdateDestroyDepartment(generics.RetrieveUpdateDestroyAPIView):
    queryset = Departments.objects.all()
    serializer_class = DepartmentSerializer
    lookup_field = 'pk'