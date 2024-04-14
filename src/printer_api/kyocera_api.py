import cups
import tempfile
import io 

from .base import BasePrinterAPI, PrinterExceptions
from ..file_handlers.document import BaseFile


class PrinterAPI(BasePrinterAPI):
    class Metadata:
        PRINTER_NAME = 'Kyocera P3145dn'
    
    conn = cups.Connection()
    
    @classmethod
    async def get_printer_capacity(cls) -> int:
        attributes = cls.conn.getPrinterAttributes(cls.Metadata.PRINTER_NAME)
        printed_sheets = int(attributes["printer-info"].get("printer-pages-printed", 0))
        return (1000 - printed_sheets) % 1000 
        
    @classmethod
    async def check_printer_cartridge(cls) -> bool:
        return True

    @classmethod
    async def print_files(cls, file: BaseFile, num_copies: int) -> None:
        print('принтим файлы')
        bytes_io: io.BytesIO = file.bytes
        
        options = {
            "copies": str(num_copies)
        }
        
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(bytes_io.getbuffer())
            temp_file_path = temp_file.name
        
        cls.conn.printFile(cls.Metadata.PRINTER_NAME, temp_file_path, "Print Job", options)
