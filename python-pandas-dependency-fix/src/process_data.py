import pandas as pd
import numpy as np

def run_pipeline():
    print("Starting data processing...")

    # Create an initial dataframe
    df = pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4, 5, 6]
    })

    # Create a new row to append
    new_row = pd.Series({'A': 4, 'B': 7})

    # ERROR SITE: .append() was removed in Pandas 2.0
    # This works in Pandas < 2.0 (e.g., 1.5.3)
    try:
        df = df.append(new_row, ignore_index=True)
        print("Row appended successfully.")
    except AttributeError as e:
        print(f"CRITICAL ERROR: {e}")
        raise e

    print(f"Final Shape: {df.shape}")
    print("Data processing completed successfully.")

if __name__ == "__main__":
    run_pipeline()