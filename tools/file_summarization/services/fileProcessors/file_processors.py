from abc import ABC, abstractmethod

class FileProcessorContext:
   
    def __init__(self, file_processor):
      self.file_processor = file_processor
    
    def get_file_processor(self):
       return self.file_processor

    def set_file_processor(self, file_processor):
      self.file_processor = file_processor

    def process(self, file_Name: str) -> str:
        return self.file_processor.process(file_Name)
    

class FileProcessorInterface(ABC):
   @abstractmethod
   def process(self, file_Name: str) -> str:
      pass