from .file_processors import FileProcessorInterface
from django.conf import settings

class TextFileProcessor(FileProcessorInterface):

    def process(self, file_name: str, chunk_size: int = 8192) -> str:
        file_name = file_name.replace(" ", "_")
        file_path = f'{settings.MEDIA_ROOT}/files/{file_name}'
        chunks = []
        
        try:
            with open(file_path, 'r') as file:
                while True:
                    chunk = file.read(chunk_size)  # Read `chunk_size` bytes at a time
                    if not chunk:  # End of file
                        break
                    chunks.append(chunk)
            
            return ''.join(chunks)  # Combine all chunks into a single string
        
        except FileNotFoundError:
            raise FileNotFoundError(f"File {file_name} not found in {settings.MEDIA_ROOT}/files/")
        except Exception as e:
            raise Exception(f"Error processing file: {str(e)}")
