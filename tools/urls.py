from django.urls import path
from .file_summarization.file_view import FileSummerizationView, QuestiouGenerationView


urlpatterns = [
    path("file-summarization/", FileSummerizationView.as_view(), name="file-summarization"),
    path("file-summarization/<fileId>", FileSummerizationView.as_view(), name="update-delete-file"),
    path("question-generation/", QuestiouGenerationView.as_view(), name="question-generation"),
]