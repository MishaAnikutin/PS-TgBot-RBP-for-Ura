import pprint
import cups
import tempfile
import io 
    
conn = cups.Connection()
pprint.pprint(conn.getPrinters())

options = {
    "copies": "1",
    "print-color-mode-default": 'color',
    'sides': 'two-sided-long-edge'
}

printers = conn.getPrinters()
printer_name = 'Kyocera_ECOSYS_P3145dn_USB'

with open("test.pdf", "rb") as fh:
    file = io.BytesIO(fh.read())
    
with tempfile.NamedTemporaryFile(delete=False) as temp_file:
    temp_file.write(file.getbuffer())    
    conn.printFile(printer_name, temp_file.name, "Print Job", options)

# scp /home/test.txt root@123.123.123.123:/directory