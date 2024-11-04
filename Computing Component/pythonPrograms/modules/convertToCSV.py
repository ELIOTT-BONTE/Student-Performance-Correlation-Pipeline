import pandas as pd
import os

def file_to_csv(input_file_path, output_file_path):
    # Determine the file extension of the input file
    _, file_extension = os.path.splitext(input_file_path)
    
    # Create output directory if it does not exist
    output_dir = os.path.dirname(output_file_path)
    if not os.path.exists(output_dir) and output_dir != "":
        os.makedirs(output_dir)
        print(f"Directory {output_dir} created.")

    # Load the file based on its extension
    if file_extension.lower() in ['.xls', '.xlsx', '.xlsm']:
        df = pd.read_excel(input_file_path, engine='openpyxl')
    elif file_extension.lower() == '.csv':
        df = pd.read_csv(input_file_path)
    else:
        raise ValueError("Unsupported file format. Please provide an Excel or CSV file.")

    # Save the dataframe to a CSV file
    df.to_csv(output_file_path, index=False)
    
    print(f"File converted successfully to {output_file_path}")
