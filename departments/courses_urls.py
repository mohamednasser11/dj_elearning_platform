from django.urls import path
from .views.courses_view import CoursesView, PurchaseCoursesView, getDepartmentCourses
from .views.lessons_view import LessonsView

urlpatterns = [
    path('', CoursesView.as_view(), name='CRUD-courses'),
    path('<int:courseId>/', CoursesView.as_view(), name='get-course'),
    path('purchase/<int:courseId>/<int:userId>/', PurchaseCoursesView.as_view(), name='purchase-course'),
    path('getDepartmentCourses/<int:departmentId>/', getDepartmentCourses.as_view(), name='get-department-courses'),
    path('<int:courseId>/lesson/<int:lessonId>/', LessonsView.as_view(), name='create-delete-edit-lessons'),
    path('<int:courseId>/', LessonsView.as_view(), name='patch-department-courses'),
]