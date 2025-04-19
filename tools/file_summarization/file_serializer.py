from rest_framework import serializers
from uuid import uuid4
from .file_models import FileUploadModel


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUploadModel
        fields = ["fileId", "fileName", "file", "created_at", "updated_at"]

    def create(self, validated_data):
        if self.context["request"].content_type in [
            "application/pdf",
            "application/text",
        ]:
            file = FileUploadModel.objects.create(
                fileId=(
                    validated_data["fileId"] if "fileId" in validated_data else uuid4()
                ),
                fileName=validated_data["fileName"],
                file=validated_data["file"],
            )

            file.save()
            return file
        else:
            raise serializers.ValidationError(
                "File type not supported. Only PDF and text files are allowed."
            )
