#!/bin/bash

# Ensure pip is available
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 not found."
    exit 1
fi

# Install test dependencies (pytest) in user mode
echo "Installing test dependencies..."
pip3 install --user pytest > /dev/null 2>&1
export PATH=$PATH:$HOME/.local/bin

# Run tests
echo "Running Tests..."
python3 -m pytest tests/test_etl.py -v