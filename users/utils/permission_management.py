from rest_framework.permissions import BasePermission


class BaseRolePermission(BasePermission):
    role_field = None
    allowed_methods = []
    admin_override = True
    message = "Permission denied"

    def has_permission(self, request, view):
        # Admin override
        if self.admin_override and request.user.is_staff:
            return True

        # Check authentication
        if not request.user.is_authenticated:
            return False

        # Check role-specific permissions
        return (
            getattr(request.user, self.role_field, False)
            and request.method in self.allowed_methods
        )
    

class InstructorPermission(BaseRolePermission):
    role_field = "instructor"
    allowed_methods = ["POST", "PATCH", "DELETE"]
    message = "Instructor permission required"

class StudentPermission(BaseRolePermission):
    role_field = "student"
    allowed_methods = ["GET", "POST"]
    message = "Student permission required"

