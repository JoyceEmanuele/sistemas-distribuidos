#!/bin/bash

if [ $# -eq 0 ]; then
    python3 scripts/client.py
else
    python3 scripts/client.py $1
fi
