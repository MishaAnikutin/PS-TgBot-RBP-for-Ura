from ..secrets.config import PRINTER_API


if PRINTER_API == 'Kyocera_ECOSYS_P3145dn':
    from .kyocera_api import PrinterAPI
    
else:
    raise KeyError(f"Incorrect {PRINTER_API = } value")


__all__ = ['PrinterAPI']
