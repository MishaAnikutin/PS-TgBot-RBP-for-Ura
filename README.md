# Print-Server with Telegram-bot client and Raspberry-pi server

**NOT STABLE VERSION!**

This template is designed for remote printing tasks, sending files to them via a telegram bot located in Raspberry-Pi and connected directly to the printer

# Installing 
firstly, connect your printer (via USB-b, Ethernet or Wi-Fi) to configured Raspberry-Pi 

Next setup and configure your Print-server
```bash 
sudo cmod +x ./setup.sh && ./setup.sh
```

Choose your printer in cli:
```bash
Выберите номер модели для подключения:
(0) HP ipp://192.168.1.1:631/printers/HP
(1) duplex ipp://192.168.1.1:631/printers/duplex
(2) HP-LaserJet-6MP ipp://192.168.1.1:631/printers/HP-LaserJet-6MP
(3) EPSON-Stylus-D78 usb://EPSON/Stylus%20D78
```

After successful setup, you will see message:
```bash
Настройка завершена!
```
## Running
```bash
python -m src.main
```

