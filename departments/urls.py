from django.urls import path
from .views.departments_views import CreateDepartments, UpdateDestroyDepartment

urlpatterns = [
    path('', CreateDepartments.as_view(), name='create-departements'),
    path('<int:pk>/', UpdateDestroyDepartment.as_view(), name='delete-getAll-update-departements'),
]