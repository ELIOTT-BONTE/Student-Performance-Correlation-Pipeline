import pandas as pd
import csv

def preprocess_grades(file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    
    # Set the first cell of the first row to "Student ID"
    df.columns.values[0] = "Student ID"

    # Identify rows where the first cell contains "Matricule" or "ECTS"
    # and drop them
    df = df[~df.iloc[:, 0].isin(["Matricule", "ECTS"])]
    
    # Reset index after dropping rows
    df.reset_index(drop=True, inplace=True)
    
    # Write the modified DataFrame back to the CSV file
    df.to_csv(file_path, index=False)
    print(f"CSV grades file has been pre processed at: {file_path}")
