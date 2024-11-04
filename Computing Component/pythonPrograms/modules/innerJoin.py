import pandas as pd

def join_csv_files(file_path1, file_path2, output_file_path):
    # Load the first CSV file into a DataFrame
    df1 = pd.read_csv(file_path1)
    df1['Student ID']=df1['Student ID'].astype(str).str.lower()
    
    # Load the second CSV file into a DataFrame
    df2 = pd.read_csv(file_path2)
    df2['Student ID']=df2['Student ID'].astype(str).str.lower()
    
    # Perform an inner join on the specified attribute
    joined_df = pd.merge(df1, df2, on="Student ID", how='inner')
    
    # Write the result of the join to a new CSV file
    joined_df.to_csv(output_file_path, index=False)
    
    print(f"Joined CSV file saved as {output_file_path}")