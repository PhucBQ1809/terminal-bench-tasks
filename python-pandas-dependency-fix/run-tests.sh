#!/bin/bash

# Install test dependencies at runtime (not in Dockerfile)
if ! command -v pytest &> /dev/null; then
    echo "Installing pytest..."
    pip install pytest --no-cache-dir
fi

# Run the tests
python3 -m pytest tests/test_outputs.py -v