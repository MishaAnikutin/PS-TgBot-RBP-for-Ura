from .base import BaseFile

      
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

