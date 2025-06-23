from django.apps import AppConfig


class DepartmentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "departments"

    def ready(self):
        from .models.departments_models import Departments
        from django.db.models.signals import post_migrate

        def add_default_categories(sender, **kwargs):
            if sender.name == self.name:
                default_categories = [
                    {"name": "Writing"},
                    {"name": "DataScience"},
                    {"name": "Photography"},
                    {"name": "ITSecurity"},
                    {"name": "Business"},
                    {"name": "Design"},
                    {"name": "Finance"},
                    {"name": "Music"},
                    {"name": "CloudComputing"},
                    {"name": "Technology"},
                    {"name": "Programming"},
                    {"name": "Health"},
                    {"name": "DevOps"},
                    {"name": "IT"},
                    {"name": "Marketing"},
                ]
                for dep in default_categories:
                    Departments.objects.get_or_create(**dep)

        post_migrate.connect(add_default_categories, sender=self)
