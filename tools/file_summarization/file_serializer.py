from rest_framework import serializers
from uuid import uuid4
from .file_models import FileUploadModel

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUploadModel
        fields = ['fileId', 'fileName', 'file', 'created_at', 'updated_at']

    def create(self, validated_data):

        file = FileUploadModel.objects.create(
            fileId=validated_data['fileId'] if 'fileId' in validated_data else uuid4(),
            fileName=validated_data['fileName'],
            file=validated_data['file'],
        )
        
        file.save()
        return file

