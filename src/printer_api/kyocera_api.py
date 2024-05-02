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
    async def print_files(cls, file: io.BytesIO, num_copies: int, two_sides: bool, color: str) -> None:     
        options = {
            "copies": str(num_copies),
            "ColorModel": 'RGB' if color.startswith('Цветная') else "Grey"
        }
        
        if two_sides:
            options['sides'] = 'two-sided-long-edge'
                
        if cls.Metadata.PRINTER_NAME not in cls.conn.getPrinters():
            raise PrinterExceptions("Не удалось подключиться к принтеру")
                
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file.getbuffer())
            print_job = cls.conn.printFile(cls.Metadata.PRINTER_NAME, temp_file.name, "Print Job", options)

        if not print_job:
            raise PrinterExceptions("Не удалось распечатать файл")
        