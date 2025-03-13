from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from departments.models.departments_models import Departments
from departments.models.serializers import CourseSerializer, DepartementSerializer


class DepratmentController:
    #GET:: get all departments
    @csrf_exempt
    def getAllDepartments(self, request):
        departements = Departments.objects.all()
        departements_serializer = DepartementSerializer(departements, many=True)
        return JsonResponse(departements_serializer.data, safe=False)
    
    #POST:: create a new department
    @csrf_exempt
    def createNewDepartment(self, request):
        departements_data = JSONParser().parse(request)
        departements_serializer = DepartementSerializer(data=departements_data)
        if departements_serializer.is_valid():
            departements_serializer.save()
            return JsonResponse('Created!', safe=False)