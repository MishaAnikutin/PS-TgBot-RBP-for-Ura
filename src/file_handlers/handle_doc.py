import re
import io 
import zipfile

from .base import BaseFile


class DocxFile(BaseFile):
    def __init__(self, file_bytes: io.BytesIO) -> None:
        self._bytes = file_bytes
        
    @property
    def bytes(self) -> io.BytesIO:
        return self._bytes
    
    def get_number_pages(self) -> int:
        with zipfile.ZipFile(self._bytes, "r") as archive:
            ms_data = archive.read("docProps/app.xml")
            app_xml = ms_data.decode("utf-8")
        
        regex = r"<(Pages|Slides)>(\d)</(Pages|Slides)>"

        matches = re.findall(regex, app_xml, re.MULTILINE)
        match = matches[0] if matches[0:] else [1, 1]
        page_count = int(match[1])

        return page_count
