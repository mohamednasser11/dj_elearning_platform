from rest_framework import serializers
from .file_models import FileUploadModel


class FileSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = FileUploadModel
        fields = [
            "fileId",
            "file",
            "level",
            "created_by",
            "number_of_questions",
            "created_at",
            "updated_at",
        ]
