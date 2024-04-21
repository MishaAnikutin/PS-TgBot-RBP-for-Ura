import io 
from types import MappingProxyType
from typing import Union

from .base import BaseFile, BasePhoto
from .handle_pdf import PDFFile
from .handle_doc import DocxFile
from .handle_image import PNGFile, JPGFile


_fileMapper = MappingProxyType({
    'docx': DocxFile,
    'pdf': PDFFile,
    'png': PNGFile,
    'jpg': JPGFile
})


ALLOWED_FORMATS = list(_fileMapper.keys()) 

def create_document(file_path: str, file_bytes: io.BytesIO, num_pages: int = 1) -> BaseFile:
    try:
        file_format = file_path.split('.')[-1]
        docBuilder: Union[BaseFile, BasePhoto] = _fileMapper[file_format]

    except (KeyError, IndexError):
        raise ValueError('invalid document type')
    
    else:
        return docBuilder(file_bytes=file_bytes, num_pages=num_pages)
