#!/bin/bash

if [ $# -eq 0 ]; then
    python3 scripts/server.py
else
    python3 scripts/server.py $1
fi
