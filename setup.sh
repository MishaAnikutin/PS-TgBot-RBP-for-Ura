#!/bin/bash
echo "--Building project--\n\n"

sudo apt update && sudo apt upgrade
sudo apt install python3 python3-pip -y
python3 -m venv venv && source ./venv/bin/activate

pip install -r requirements.txt

# for cups
sudo apt install libcups2-dev
sudo apt install python3-dev

git clone https://github.com/OpenPrinting/pycups.git
sudo python3 pycups/setup.py install
pip install pycups

sudo apt install cups
sudo service cups start

echo "--The project is ready to start--"

python3 setup.py

