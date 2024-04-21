import cups
import tempfile
import io 

from .base import BasePrinterAPI, PrinterExceptions
from ..file_handlers.document import BaseFile


class PrinterAPI(BasePrinterAPI):
    class Metadata:
        PRINTER_NAME = 'Kyocera_ECOSYS_P3145dn_'
    
    conn = cups.Connection()
    
    @classmethod
    async def get_printer_capacity(cls) -> int:
        return 1000 
        
    @classmethod
    async def check_printer_cartridge(cls) -> bool:
        return True

    @classmethod
    async def print_files(cls, file: io.BytesIO, num_copies: int) -> None:     
        options = {"copies": str(num_copies)}
        
        print(file)       
        
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file.getbuffer())
            cls.conn.printFile(cls.Metadata.PRINTER_NAME, temp_file.name, "Print Job", options)
