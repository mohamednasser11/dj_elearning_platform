import uuid
from django.db import models

class FileUploadModel(models.Model):
    fileId = models.UUIDField(primary_key=True, editable=False)
    file = models.FileField(upload_to='files/')
    fileName = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file_name
    
    class Meta:
        verbose_name = 'file Upload'
        verbose_name_plural = 'files Upload'