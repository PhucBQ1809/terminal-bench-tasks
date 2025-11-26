#!/bin/bash

echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "Running data pipeline..."
python3 src/process_data.py