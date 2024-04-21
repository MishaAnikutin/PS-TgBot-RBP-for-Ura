import io
from .base import BasePhoto

      
class JPGFile(BasePhoto):
    def __init__(self, file_bytes: io.BytesIO, num_pages: int) -> None:
        self._number_pages = num_pages
        self._photo_bytes = file_bytes
    
    @property
    def bytes(self):
        return self._photo_bytes
    
    def get_number_pages(self) -> int:
        return self._number_pages
    
    
class PNGFile(BasePhoto):
    def __init__(self, file_bytes: io.BytesIO, num_pages: int) -> None:
        self._number_pages = num_pages
        self._photo_bytes = file_bytes
    
    @property
    def bytes(self):
        return self._photo_bytes
    
    def get_number_pages(self) -> int:
        return self._number_pages

