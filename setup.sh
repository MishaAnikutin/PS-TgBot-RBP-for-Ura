#!/bin/bash

echo "--building project--"

sudo apt-update
sudo apt install python3 python3-pip -y
python3 -m venv venv && source ./venv/bin/activate
pip install -r requirements.txt

echo "--project is ready--"