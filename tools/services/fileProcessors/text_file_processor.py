from .file_processors import FileProcessorInterface
from django.conf import settings

class TextFileProcessor(FileProcessorInterface):

    def process(self, file_Name: str) -> str:
        file_Name = file_Name.replace(" ", "_")
        linesArray = []
        with open(f'{settings.MEDIA_ROOT}/files/{file_Name}', 'r') as file:
            for line in file:
                linesArray.append(line)

        return str(linesArray)
