#!/bin/bash
cd ./src


if [ -x "$(command -v py)" ]; then
    py ./main.py
elif [ -x "$(command -v py)" ]; then
    python3 ./main.py 
elif [ -x "$(command -v py)" ]; then
    python ./main.py
else 
    echo "No available version of Python was found!"
fi
