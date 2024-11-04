# Drops empty columns from a CSV file

import pandas as pd

def delete_empty_columns(file):
    # Read CSV file
    df = pd.read_csv(file)

    # Identify columns that are either completely empty or full of spaces
    columns_to_drop = [col for col in df.columns if df[col].replace(" ", pd.NA).isna().all()]
    
    # Drop these columns
    df.drop(columns=columns_to_drop, inplace=True)

    # Save modified CSV
    df.to_csv(file)
    print(f"Empty columns dropped in {file}")