import io
from PyPDF2 import PdfReader

from .base import BaseFile


class PDFFile(BaseFile):
    def __init__(self, file_bytes: io.BytesIO) -> None:
        self._bytes = file_bytes
        self._file = PdfReader(file_bytes)    
    
    @property
    def bytes(self) -> io.BytesIO:
        return self._bytes

    def get_number_pages(self) -> int:
        return len(self.file.pages)
