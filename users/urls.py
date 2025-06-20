from django.urls import path
from .views import auth_views, user_views, instructor_views

urlpatterns = [
    path("register/", auth_views.UserCreateView.as_view(), name="register-users"),
    path("login/", auth_views.LoginView.as_view(), name="login-users"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout-users"),
    path("getAllStudents/", user_views.StudentsView.as_view(), name="get-all-students"),
    path("getAllInsturctors/", instructor_views.InstructorFreelanceView.as_view(), name="get-all-instructors"),
    path("applyToFreelance/<int:userId>/", instructor_views.InstructorFreelanceView.as_view(), name="apply-to-freelance"),
    path("getInsturctor/<int:userId>/", instructor_views.InstructorFreelanceView.as_view(), name="get-instructor-by-id"),
]
