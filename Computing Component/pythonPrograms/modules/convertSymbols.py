import pandas as pd

# parses through a CSV and changes symbols denoting presence by "P" and absence by "A"

def convert_symbols(attendance_file):
    # Load CSV as dataframe
    df = pd.read_csv(attendance_file)

    # Replace symbols for presence
    values_for_presence = ["x", "y", "P (2/2)", "X"]

    for value in values_for_presence:
        df = df.replace(value, "P")

    # Replace symbols for absence
        
    values_for_absence = ["A (0/2)", "E (1/2)", " ", "None"]

    for value in values_for_absence:
        df = df.replace(value, "A")
    
    # Fill empty cells with "A"
    # df.fillna("A", inplace=True)

    # Overwrite the original file
    df.to_csv(attendance_file)
    print(f"Symbols converted successfuly in file {attendance_file}")