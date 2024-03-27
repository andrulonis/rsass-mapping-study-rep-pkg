#!/bin/bash


PYTHON_CMD=""
if [ "$1" == "--python3" ]; then
    echo "Using Python 3"
    PYTHON_CMD=python3
elif [ "$1" == "--python" ]; then
    echo "Using Python (assumed to be Python 3)"
    PYTHON_CMD=python
else
    echo "Invalid argument. Please specify 'python3' or 'python'."
    exit 1
fi


$PYTHON_CMD -m venv rsas_venv

source rsas_venv/bin/activate

$PYTHON_CMD -m pip install -r requirements.txt

$PYTHON_CMD src/proceedings_collection.py

$PYTHON_CMD src/proceedings_collection.py --pilot

$PYTHON_CMD src/pilots_and_final.py

$PYTHON_CMD src/generate_plots.py