# Generated by Django 5.1.7 on 2025-03-10 21:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('departments', '0002_alter_course_departmentid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['created_at'], 'verbose_name': 'Course', 'verbose_name_plural': 'Courses'},
        ),
    ]
