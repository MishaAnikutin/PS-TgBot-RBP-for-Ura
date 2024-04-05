from ..secrets.config import PRINTER_API


if PRINTER_API == "kyocera":
    from .kyocera_api import PrinterAPI
    
else:
    raise KeyError(f"Incorrect {PRINTER_API = } value")


__all__ = ['PrinterAPI']
