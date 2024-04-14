# Print-Server with Telegram-bot client and Raspberry-pi server

**NOT STABLE VERSION!**

This template is designed for remote printing tasks, sending files to them via a telegram bot located in Raspberry-Pi and connected directly to the printer

# Installing 
firstly, connect your printer (via USB-b, Ethernet or Wi-Fi) to configured Raspberry-Pi 

```bash 
sudo cmod +x ./setup.sh && ./setup.sh
```

## Running
```bash
python -m src.main
```

