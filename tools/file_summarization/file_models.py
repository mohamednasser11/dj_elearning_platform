import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings

User = get_user_model()


class FileUploadModel(models.Model):
    fileId = models.UUIDField(
        primary_key=True, editable=False, default=uuid.uuid4, auto_created=True
    )
    file = models.FileField(upload_to="files/")
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="file_uploads"
    )
    level = models.CharField(max_length=50)
    number_of_questions = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "file Upload"
        verbose_name_plural = "files Upload"
