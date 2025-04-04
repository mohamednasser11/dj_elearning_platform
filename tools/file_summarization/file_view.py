from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .file_models import FileUploadModel
from .file_serializer import FileSerializer
from .services.fileProcessors.file_processors import FileProcessorContext
from .services.fileProcessors.pdf_file_processor import PDFProcessor
from .services.fileProcessors.text_file_processor import TextFileProcessor
from ..AI.AI_model_service import AIModelService


class fileSummerizationView(APIView):
    queryset = FileUploadModel.objects.all()
    serializer_class = FileSerializer

    def get(self, request, fileId):
        try:
            if fileId is not None:
                file = self.queryset.objects.get(id=fileId)
                fileSerializer = self.serializer_class(file)
                print(f"fileSerializer: {fileSerializer.data}")
                if fileSerializer.is_valid():
                    return Response(fileSerializer.data, status=status.HTTP_200_OK)
                return Response(
                    "This is the file summerization view", status=status.HTTP_200_OK
                )
            else:
                return Response(
                    "This is the file summerization view", status=status.HTTP_200_OK
                )
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            fileSerializer = FileSerializer(data=request.data)
            print(f"fileSerializer: {fileSerializer}")
            if fileSerializer.is_valid():
                # file_processor = None
                file_processor_types = {
                    "application/pdf": PDFProcessor(),
                    "application/text": TextFileProcessor(),
                }
                if file_processor_types.get(
                        fileSerializer.validated_data["file"].content_type
                    ):
                    file_processor = file_processor_types.get(
                        fileSerializer.validated_data["file"].content_type
                    )
                else:
                    return Response('File Processor Not implemented', status=status.HTTP_400_BAD_REQUEST)
                
                file_context = FileProcessorContext(file_processor)
                fileSerializer.save()
                processedText = file_context.process(fileSerializer.validated_data["file"].name)
                print(f"processedText: {processedText}")
                if processedText:
                    #save and send processed text to AI model
                    ai_model_service = AIModelService()
                    response = ai_model_service.generate(f"check this data and summarize it: {processedText}")
                    return Response(response, status=status.HTTP_201_CREATED)
                else:
                    return Response('File not processed', status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    fileSerializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        try:
            return Response(
                "This is the file summerization view", status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        try:
            return Response(
                "This is the file summerization view", status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
