from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from .models.course_models import Course
from .models.departments_models import Departments
from .serializers import CourseSerializer, DepartementSerializer

# Create your views here.
@csrf_exempt
def home(request):
    if request.method == 'GET':
        departements = Departments.objects.all()
        departements_serializer = DepartementSerializer(departements, many=True)
        return JsonResponse(departements_serializer.data, safe=False)