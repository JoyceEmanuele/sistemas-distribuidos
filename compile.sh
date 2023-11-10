#!/bin/bash

# install pip
sudo apt-get update
sudo apt-get install python-pip

# install dependencies project step 1
pip install cachetools 
pip install grpcio-tools
pip3 install paho-mqtt

# install dependencies project step 1
pip install plyvel
pip install pysyncobj