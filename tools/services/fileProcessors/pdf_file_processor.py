import fitz
from django.conf import settings
from .file_processors import FileProcessorInterface


class PDFProcessor(FileProcessorInterface):

    def process(self, file_name: str, max_chunk_size: int = 4096) -> str:
        """
        Processes a PDF file in chunks (page-by-page or smaller text blocks).

        Args:
            file_name (str): Name of the PDF file.
            max_chunk_size (int): Approximate max size of each text chunk (in chars).

        Returns:
            str: Concatenated text from all chunks.
        """
        file_name = file_name.replace(" ", "_")
        file_path = f"{settings.MEDIA_ROOT}/files/{file_name}"
        chunks = []

        try:
            doc = fitz.open(file_path)
            for page in doc:
                text = page.get_text()
                # Split page text into smaller chunks if needed
                for i in range(0, len(text), max_chunk_size):
                    chunk = text[i : i + max_chunk_size]
                    chunks.append(chunk)
            return "".join(chunks)

        except FileNotFoundError:
            raise FileNotFoundError(f"PDF file {file_name} not found.")
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")
