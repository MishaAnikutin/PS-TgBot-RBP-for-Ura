from abc import ABC, abstractclassmethod, abstractproperty
from ..file_handlers.document import BaseFile


class BasePrinterAPI(ABC):
    @abstractproperty
    def printer_type(self):
        ...
    
    @abstractclassmethod
    def get_printer_capacity(cls) -> int:
        ...
        
    @abstractclassmethod
    def check_printer_cartridge(cls) -> bool:
        ...

    @abstractclassmethod
    def print_files(cls, file: BaseFile, num_copies: int) -> None:
        ...

class PrinterExceptions(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f'PrinterExceptions: {self.message}'