# Compute the total number of presences per student, along with their percentage

import pandas as pd

def compute_sessions_attended(file):
    # Load the CSV file
    df = pd.read_csv(file)
    
    # Function to count "P" in each row
    def count_P(row):
        return sum(cell == 'P' for cell in row)
    
    # Apply the function across the dataframe, axis=1 makes it go row by row
    df['sessionsAttended'] = df.apply(count_P, axis=1)
    
    # Count columns that contain at least one 'P'
    # This is to have a total number of sessions
    total_sessions = sum(df.apply(lambda col: "P" in col.values, axis=0))
    print(f"Number of sessions from the course: {total_sessions}")
    
    
    # Calculate attendance percentage for each row
    if total_sessions > 0:  # To avoid division by zero
        df['attendancePercentage'] = df['sessionsAttended'] / total_sessions * 100
    else:
        df['attendancePercentage'] = 0  # If there are no columns with 'P', set percentage to 0
    
    # Save the updated dataframe back to a CSV file
    df.to_csv(file, index=False)
    print(f"Sessions number computed and saved in CSV file at: {file}")