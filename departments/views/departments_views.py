from rest_framework import generics, status
from rest_framework.response import Response 
from rest_framework.views import APIView
from departments.models.departments_models import Departments
from ..serializers.departments_serializer import DepartmentSerializer


class CreateDepartments(generics.ListCreateAPIView):
    queryset = Departments.objects.all()
    serializer_class = DepartmentSerializer

    def post(self, request):
        super().post(request)
        return Response({"message": "created successfully"}, status=status.HTTP_201_CREATED)


class UpdateDestroyDepartment(generics.RetrieveUpdateDestroyAPIView):
    queryset = Departments.objects.all()
    serializer_class = DepartmentSerializer
    lookup_field = 'pk'

    def patch(self, request, *args, **kwargs):
        super().patch(request, *args, **kwargs)
        return Response({"message": "updated successfully"}, status=status. HTTP_204_NO_CONTENT)
    
    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return Response({"message": "deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        return Response({"message": "retrieved successfully"}, status=status.HTTP_200_OK)