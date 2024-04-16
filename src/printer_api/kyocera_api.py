# import cups
import tempfile
import io 

from .base import BasePrinterAPI, PrinterExceptions
from ..file_handlers.document import BaseFile


class PrinterAPI(BasePrinterAPI):
    class Metadata:
        PRINTER_NAME = 'Kyocera_ECOSYS_P3145dn_'
    
    # conn = cups.Connection()
    
    @classmethod
    async def get_printer_capacity(cls) -> int:
        #TODO: определить число страниц в принтере
        # attributes = cls.conn.getPrinterAttributes(cls.Metadata.PRINTER_NAME)
        # from pprint import pprint
        
        # pprint(attributes)
        
        # printed_sheets = int(attributes["printer-info"].get("printer-pages-printed", 0))
        return 1000 
        
    @classmethod
    async def check_printer_cartridge(cls) -> bool:
        return True

    @classmethod
    async def print_files(cls, file: io.BytesIO, num_copies: int) -> None:
        ...     
        # options = {
        #     "copies": str(num_copies)
        # }
        
        # with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        #     temp_file.write(file.getbuffer())
        #     temp_file_path = temp_file.name
        
        # cls.conn.printFile(cls.Metadata.PRINTER_NAME, temp_file_path, "Print Job", options)
