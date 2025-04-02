import fitz
from django.conf import settings
from .file_processors import FileProcessorInterface


class PDFProcessor(FileProcessorInterface):

    def process(self, file_Name: str) -> str:

        file_Name = file_Name.replace(" ", "_")
        doc = fitz.open(f'{settings.MEDIA_ROOT}/files/{file_Name}')

        return "".join(page.get_text() for page in doc)