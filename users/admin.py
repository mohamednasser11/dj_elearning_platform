from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models.user_model import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email',  'is_student')
    list_filter = ['is_student']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',  'is_student', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )