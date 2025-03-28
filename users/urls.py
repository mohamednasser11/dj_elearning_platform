from django.urls import path
from .views import auth_views, user_views

urlpatterns = [
    path("register/", auth_views.UserCreateView.as_view(), name="register-users"),
    path("login/", auth_views.LoginView.as_view(), name="login-users"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout-users"),
    path("getAllStudents/", user_views.StudentsView.as_view(), name="get-all-students"),
    path("getAllInsturctors/", user_views.InstructorsView.as_view(), name="get-all-students"),
]
