import io 
from types import MappingProxyType

from .base import BaseFile
from .handle_pdf import PDFFile
from .handle_doc import DocxFile
from .handle_image import PNGFile, JPGFile

# static typing dict
docMapper = MappingProxyType({
    'pdf': PDFFile,
    # 'docx': DocxFile,
    # 'png': PNGFile,
    # 'jpg': JPGFile
})

ALLOWED_FORMATS = list(docMapper.keys())


def create_document(file_path: str, file_bytes: io.BytesIO) -> BaseFile:
    try:
        file_format = file_path.split('.')[-1]
        docBuilder: BaseFile = docMapper[file_format]

    except (KeyError, IndexError):
        raise ValueError('invalid document type')
    
    else:
        return docBuilder(file_bytes=file_bytes)
