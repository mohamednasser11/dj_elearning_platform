from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from departments.controllers.departments_controller import DepratmentController


# Create your views here.
@csrf_exempt
def departementsHandler(request):
    try:
        incoming_requests = {
        "GET": DepratmentController().getAllDepartments,
        "POST": DepratmentController().createNewDepartment
       }

        return incoming_requests[request.method](request)
    except:
        print('Error Occured!')

@csrf_exempt
def coursesHandler(request):
    NotImplemented