# Generated by Django 5.1.7 on 2025-03-27 05:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('departments', '0005_rename_coursesofdepratment_coursesofdepartment'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoursesLesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('video', models.FileField(upload_to='courses_lessons/videos/')),
                ('duration', models.DurationField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='departments.course')),
            ],
            options={
                'verbose_name': 'Course Lesson',
                'verbose_name_plural': 'Course Lessons',
            },
        ),
    ]
