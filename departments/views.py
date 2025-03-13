from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics

from departments.controllers.departments_controller import DepratmentController
from departments.models.departments_models import Departments
from departments.models.serializers import DepartementSerializer


class CreateDepartments(generics.ListCreateAPIView):
    queryset = Departments.objects.all()
    serializer_class = DepartementSerializer


class UpdateDestroyDepartment(generics.RetrieveUpdateDestroyAPIView):
    queryset = Departments.objects.all()
    serializer_class = DepartementSerializer
    lookup_field = 'pk'