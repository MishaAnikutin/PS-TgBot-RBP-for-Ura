# Print-Server with Telegram-bot client and Raspberry-pi server

**NOT STABLE VERSION!**

# Architecture:
[Figma's board](https://www.figma.com/file/xJomjKpzGFbDnQwvDVy4LW/%D0%9E%D0%B1%D0%BB%D0%B0%D1%87%D0%BD%D0%B0%D1%8F-%D0%B0%D1%80%D1%85%D0%B8%D1%82%D0%B5%D0%BA%D1%82%D1%83%D1%80%D0%B0-Digital-Typography?type=whiteboard&node-id=0-1&t=iMTPc3xABizq2heL-0)

This template is designed for remote printing tasks, sending files to them via a telegram bot located in Raspberry-Pi and connected directly to the printer

# Installing 
firstly, connect your printer (via USB-b using instructions: https://dzen.ru/a/YyX2FnNQynfDVGn2)

to configured Raspberry-Pi 

Secondly, clone this repository to your Raspberry-Pi:
```bash
git clone https://github.com/MishaAnikutin/PS-TgBot-RBP-for-Ura.git
```

Next step, run setup script
```bash 
sudo cmod +x ./setup.sh && ./setup.sh
```
It will install all requirements

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

