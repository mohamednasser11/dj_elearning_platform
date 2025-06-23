import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .file_models import FileUploadModel
from .file_serializer import FileSerializer
from ..services.fileProcessors.file_processors import FileProcessorContext
from ..services.fileProcessors.pdf_file_processor import PDFProcessor
from ..services.fileProcessors.text_file_processor import TextFileProcessor
from ..AI.AI_model_service import AIModelService


def get_file_processor(file):
    file_processor_types = {
        "application/pdf": PDFProcessor(),
        "text/plain": TextFileProcessor(),
    }
    return file_processor_types.get(file.content_type, None)


class FileSummerizationView(APIView):
    queryset = FileUploadModel.objects.all()
    serializer_class = FileSerializer
    permission_classes = []

    def get(self, _, fileId):
        try:
            file = self.queryset.get(id=fileId)
            if file.is_deleted is False:
                return Response(
                    self.serializer_class(file).data, status=status.HTTP_200_OK
                )
            return Response(
                "This file doesn't exist or deleted",
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serialized_file = self.serializer_class(
                data=request.data, context={"request": request}
            )
            if serialized_file.is_valid():
                file_processor = get_file_processor(
                    serialized_file.validated_data["file"]
                )

                if file_processor is None:
                    return Response(
                        "File Processor Not implemented",
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                try:
                    serialized_file.save()
                    instance = serialized_file.instance

                    file_context = FileProcessorContext(file_processor)
                    processed_text = file_context.process(
                        os.path.basename(instance.file.name)
                    )

                    model = AIModelService()
                    response = model.generate(
                        f"""
                            You are an AI-assistant designed to help students working on their subjects and studies.
                            Your task is to summarize the provided document into concise bullet points that capture the key information and concepts.
                            Follow the strict output format and requirements below to ensure clarity and relevance.
                            Do not behave as a chatbot or humanize your response. you are only getting one request per user so there is no interactions.
                            SYSTEM INSTRUCTION:
                            Summarize the following document into bullet points. The length of the summary should be `{instance.level}`.

                            STRICT OUTPUT FORMAT:
                            - Plain text with '-' for the bullets
                            - Begin IMMEDIATELY with bullet points
                            - Zero introductory/closing text

                            DOCUMENT:
                            {processed_text}
                        """
                    )
                    return Response(response, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    serialized_file.errors, status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, _, fileId):
        try:
            file = self.queryset.get(id=fileId)
            if file:
                file.is_deleted = True
                file.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class QuestionGenerationView(APIView):
    queryset = FileUploadModel.objects.all()
    serializer_class = FileSerializer
    permission_classes = []

    def post(self, request):
        try:
            serialized_file = self.serializer_class(
                data=request.data, context={"request": request}
            )
            if serialized_file.is_valid():
                file_processor = get_file_processor(
                    serialized_file.validated_data["file"]
                )

                if file_processor is None:
                    return Response(
                        "File Processor Not implemented",
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                try:
                    serialized_file.save()
                    instance = serialized_file.instance

                    file_context = FileProcessorContext(file_processor)
                    processed_text = file_context.process(
                        os.path.basename(instance.file.name)
                    )

                    model = AIModelService()
                    response = model.generate(
                        f"""
                            SYSTEM INSTRUCTION:
                            Generate exactly `{instance.number_of_questions}` exam questions at `{instance.level}` difficulty.

                            STRICT OUTPUT FORMAT:
                            - Plain text
                            - Begin IMMEDIATELY with Question 1
                            - Zero introductory/closing text
                            - Format
                                ```  
                                [Question X] [Type]
                                [Question text]
                                [Answer]
                                ```

                            QUESTION REQUIREMENTS:
                            - Vary types
                                - `MC` (Multiple Choice): 4 options
                                - `TF` (True/False): State assertion clearly
                                - `SA` (Short Answer): Phrase to require 1-2 word responses
                            - Content constraints
                                - Test ONLY core concepts from provided text
                                - Exclude peripheral/external knowledge

                            DOCUMENT:
                            {processed_text}
                        """
                    )
                    return Response(response, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    serialized_file.errors, status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
