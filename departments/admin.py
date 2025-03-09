from django.contrib import admin
from .models.course_models import Course
from .models.departments_models import Departments
# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('courseId', 'title', 'departmentId', 'instructorId', 'price', 'created_at')
    
    # Fields to filter by in the right sidebar
    list_filter = ('departmentId', 'instructorId', 'created_at')
    
    # Fields to search by in the search bar
    search_fields = ('title', 'description')
    
    # Fields to prepopulate (if applicable)
    #prepopulated_fields = {'slug': ('title',)}  # Optional: If you have a slug field
    
    # Fields to display in the detail/edit view
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'departmentId', 'instructorId', 'price')
        }),
        ('Advanced Options', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at'),
        }),
    )
    
    # Read-only fields (e.g., timestamps)
    readonly_fields = ('created_at', 'updated_at')
    
    # Ordering in the list view
    ordering = ('-created_at',)  # Newest courses first

@admin.register(Departments)
class DepartementAdmin(admin.ModelAdmin):
    list_display = ('departmentId', 'name')
    list_filter = ('departmentId', 'name')
    search_fields = ('departmentId', 'name')

    fieldsets = (
        (None, {
            'fields': ('departmentId', 'name')
        }),
    )