from django.urls import path
from .file_summarization.file_view import fileSummerizationView


urlpatterns = [
    path("file-summarization/", fileSummerizationView.as_view(), name="file-summarization"),
]