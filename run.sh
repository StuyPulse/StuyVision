#!/bin/bash
cd ./src


if [ -x "$(command -v python3)" ]; then
    python3 ./main.py 
elif [ -x "$(command -v python)" ]; then
    python ./main.py
elif [ -x "$(command -v py)" ]; then
    py ./main.py
else 
    echo "No available version of Python was found!"
fi
