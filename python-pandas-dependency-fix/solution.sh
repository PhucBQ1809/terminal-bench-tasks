#!/bin/bash

# The issue is that pandas 2.0+ removed the 'append' method.
# The proper DevOps fix is to pin the dependency to a compatible legacy version.
# CRITICAL FIX: We must also pin numpy<2 because pandas 1.5.3 is incompatible with numpy 2.0+

echo "Fixing requirements.txt to use pandas 1.5.3 and numpy < 2..."
cat << 'EOF' > requirements.txt
pandas==1.5.3
numpy<2
EOF

echo "Re-installing fixed dependencies..."
# Force reinstall to ensure we downgrade numpy if version 2 was already installed
pip install -r requirements.txt --force-reinstall

echo "Verifying fix..."
python3 src/process_data.py