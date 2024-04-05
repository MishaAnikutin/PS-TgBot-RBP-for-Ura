from PyPDF2 import PdfReader
from .base import BaseFile

ALLOWED_FORMATS = ['pdf', 'doc', 'docx']     


   
class PDFFile(BaseFile):
    def __init__(self, file_bytes: bytes = None) -> None:
        self.file_bytes = file_bytes
        self.file = PdfReader(file_bytes)
    
    @property
    def bytes(self):
        return self.file_bytes

    def get_number_pages(self) -> int:
        return len(self.file.pages)


class DocFile(BaseFile):
    def __init__(self, file_bytes: bytes = None) -> None:
        raise NotImplementedError
    
    @property
    def bytes(self):
        return self.file_bytes
    
    def get_number_pages(self) -> int:
        return 1

        
class DocxFile(BaseFile):
    def __init__(self, file_bytes: bytes = None) -> None:
        raise NotImplementedError
    
    @property
    def bytes(self):
        return self.file_bytes

    def get_number_pages(self) -> int:
        return 1

        
class JPGFile(BaseFile):
    def __init__(self, file_bytes: bytes = None) -> None:
        raise NotImplementedError
    
    @property
    def bytes(self):
        return self.file_bytes

    def get_number_pages(self) -> int:
        return 1
    
    
class PNGFile(BaseFile):
    def __init__(self, file_bytes: bytes = None) -> None:
        raise NotImplementedError
    
    @property
    def bytes(self):
        return self.file_bytes
    
    def get_number_pages(self) -> int:
        return 1


def create_document(file_path: str, file_bytes: bytes) -> BaseFile:
    if file_path.endswith('.pdf'):
        return PDFFile(file_bytes=file_bytes)
    elif file_path.endswith('.doc'):
        return DocFile(file_bytes=file_bytes)
    elif file_path.endswith('.docx'):
        return DocxFile(file_bytes=file_bytes)

    raise ValueError('invalid document type')
    