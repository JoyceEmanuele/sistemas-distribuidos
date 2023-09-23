#!/bin/bash

# install pip
sudo apt-get update
sudo apt-get install python-pip

# install dependencies
pip install cachetools 
pip install grpcio-tools
pip3 install paho-mqtt