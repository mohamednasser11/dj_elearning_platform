from django.db import migrations
from django.contrib.auth.models import Group, Permission

def create_groups_and_permissions(apps, schema_editor):
    # Create a group for instructors
    instructor_group, created = Group.objects.get_or_create(name='Instructors')

    # Add permissions to the group
    try:
        permission = Permission.objects.get(codename='add_departments')
        instructor_group.permissions.add(permission)
    except Permission.DoesNotExist:
        print("Permission 'add_departments' does not exist. Skipping.")

class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),  # Replace with the previous migration file
    ]

    operations = [
        migrations.RunPython(create_groups_and_permissions),
    ]