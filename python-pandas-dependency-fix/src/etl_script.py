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
