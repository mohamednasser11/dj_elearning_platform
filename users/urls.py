from django.urls import path
from .views import auth_views

urlpatterns = [
    path('register/', auth_views.UserCreateView.as_view(), name='register-users'),
    path('login/', auth_views.LoginView.as_view(), name='login-users'),
]
