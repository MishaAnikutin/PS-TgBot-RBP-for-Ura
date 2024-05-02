import os
import cups

    
def cli():
    conn = cups.Connection()
    printers = conn.getPrinters()

    if printers is None:
        print("Ни один принтер не подключен. Подключите принтер и повторите команду: python3 setup.py")
        return

    print("Выберите номер модели для подключения:")
    for i, printer in enumerate(printers) :
        print(f'({i}) {printer}, {printers[printer]["device-uri"]}')
    
    while True:
        try:
            i = int(input())
            model = list(printers.keys())[i]
        except:
            print("Введите номер модели!")
        else:
            break
    
    os.environ["PRINTER_API"] = model
    print("Настройка завершена успешно!")


if __name__ == "__main__":
    cli()
