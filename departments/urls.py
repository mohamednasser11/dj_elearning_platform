from django.urls import path
from .views.departments_views import CreateDepartments, UpdateDestroyDepartment
from .views.courses_view import CoursesView, PurchaseCoursesView, getDepartmentCourses
from .views.lessons_view import LessonsView

urlpatterns = [
    path('', CreateDepartments.as_view(), name='create-departements'),
    path('<int:pk>/', UpdateDestroyDepartment.as_view(), name='delete-getAll-update-departements'),
    path('courses/', CoursesView.as_view(), name='CRUD-courses'),
    path('courses/<int:pk>/', CoursesView.as_view(), name='get-course'),
    path('courses/<int:courseId>/<int:userId>/', PurchaseCoursesView.as_view(), name='purchase-course'),
    path('courses/getDepartmentCourses/<int:departmentId>/', getDepartmentCourses.as_view(), name='get-department-courses'),
    path('courses/<int:courseId>/<int:lessonId>/', LessonsView.as_view(), name='create-delete-edit-lessons'),
    path('courses/<int:courseId>/', LessonsView.as_view(), name='patch-department-courses'),
]