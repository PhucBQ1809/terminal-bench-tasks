#!/bin/bash

echo "Starting Solution Application..."

# 1. Define backup directory to safely store original files
BACKUP_DIR="backup_$(date +%s)"
mkdir -p "$BACKUP_DIR"
echo "Backup directory created: $BACKUP_DIR"

# 2. Backup original source
cp src/etl_script.py "$BACKUP_DIR/etl_script.py.bak"
cp requirements.txt "$BACKUP_DIR/requirements.txt.bak"
echo "Original files backed up."

# 3. Create a temporary build/test environment
# Using /tmp ensures no permission issues with host volume mounts
WORK_DIR=$(mktemp -d)
echo "Working in temp directory: $WORK_DIR"
cp src/etl_script.py "$WORK_DIR/etl_script.py"

# 4. Refactor Code: Replace .append() with pd.concat()
# This logic collects dfs in a list and concats them once (efficient & modern)
echo "Refactoring Python code..."
cat > src/etl_script.py << 'EOF'
import pandas as pd
import numpy as np
import sys

def process_data():
    print("Starting ETL Process...")

    # Fix: Use a list to store dataframes, then concat
    dfs = []

    # Simulate processing batches of data
    for i in range(5):
        new_data = {
            'id': [i],
            'value': [np.random.rand()],
            'category': ['A' if i % 2 == 0 else 'B']
        }
        batch_df = pd.DataFrame(new_data)
        dfs.append(batch_df)

    # Use pd.concat instead of deprecated .append
    if dfs:
        df = pd.concat(dfs, ignore_index=True)
    else:
        df = pd.DataFrame(columns=['id', 'value', 'category'])

    print("Aggregating data...")
    result = df.groupby('category')['value'].mean()
    print("Results:\n", result)

    print("ETL Process Completed Successfully.")

if __name__ == "__main__":
    try:
        process_data()
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        sys.exit(1)
EOF

# 5. Fix requirements.txt: Pin versions
echo "Pinning dependencies in requirements.txt..."
# Gets the currently installed pandas version to pin it accurately or sets a fixed valid one
CURRENT_PANDAS=$(python3 -c "import pandas; print(pandas.__version__)" 2>/dev/null || echo "2.1.0")
cat > requirements.txt << EOF
pandas==$CURRENT_PANDAS
numpy>=1.24.0
pytest==7.4.0
EOF

# 6. Verify syntax of the new script (Dry run)
echo "Verifying Python syntax..."
python3 -m py_compile src/etl_script.py
if [ $? -eq 0 ]; then
    echo "Syntax verification passed."
else
    echo "Syntax error in patched file!"
    rm -rf "$WORK_DIR"
    exit 1
fi

# 7. Re-install dependencies to ensure environment matches requirements
echo "Updating environment..."
pip3 install --user -r requirements.txt

# 8. Clean up temp directory
rm -rf "$WORK_DIR"
echo "Cleanup complete."

# 9. Final message
echo "Solution applied: Code refactored to use pd.concat and dependencies pinned."