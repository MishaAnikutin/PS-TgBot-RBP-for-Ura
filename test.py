import cups

    
conn = cups.Connection()
printers = conn.getPrinters()

for printer in printers:
    print(f'- {printer}, {printers[printer]["device-uri"]}')
