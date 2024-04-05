from .base import BasePrinterAPI
from ..file_handlers.document import BaseFile


class PrinterAPI(BasePrinterAPI):
    printer_type = 'Kyocera P3145dn 1102TT3NL0'
    
    
    @classmethod
    async def get_printer_capacity(cls) -> int:
        return 150

    @classmethod
    async def check_printer_cartridge(cls) -> bool:
        return True

    @classmethod
    async def print_files(cls, file: BaseFile, num_copies: int) -> None:
        print('принтим файлы')
