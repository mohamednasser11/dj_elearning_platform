from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from departments.controllers.departments_controller import DepratmentController


# Create your views here.
@csrf_exempt
def departementsHandler(request):

    if request.method == "GET":
        return DepratmentController().getAllDepartments(request)
    elif request.method == "POST":
        return DepratmentController().createNewDepartment(request)
