import pandas as pd
import matplotlib.pyplot as plt

def makeSummaryTable(*courses, save_to_csv=True, csv_filename="pythonPrograms/output/Summary.csv", save_to_png=True, png_filename="pythonPrograms/output/Summary.png"):
    """
    Create a DataFrame from given course data and optionally save it to a CSV file.
    
    Parameters:
    - courses: An arbitrary number of tuples, each representing course data.
    - save_to_csv: Boolean, if True the DataFrame is saved to a CSV file.
    - csv_filename: The filename for the CSV file (default is 'courses_data.csv').
    
    Returns:
    - A pandas DataFrame containing the course data.
    """
    # Column headers
    headers = [
        "Course Name", 
        "Session type",
        "Attendance-Grade correlation", 
        "p-value", 
        "Student fail rate", 
        "Student absence rate", 
        "Average attendance percentage", 
        "Average grade", 
        "Student count",
        "Classification"
    ]

    # Create DataFrame
    df = pd.DataFrame(courses, columns=headers)
    
    # Print the DataFrame
    print(df)

    # Save the DataFrame to a CSV file if requested
    if save_to_csv:
        df.to_csv(csv_filename, index=False)

    # Save the DataFrame as a PNG file if requested
    if save_to_png:
        fig, ax = plt.subplots(figsize=(20, 8))  # Adjust the size as needed
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(2, 2)  # Adjust scaling to fit the content better (now set to 2 because "HCI (Human Computer Interactions)" takes so much space in table)

        plt.savefig(png_filename, bbox_inches='tight')
        plt.close()
    
    return df

# Example usage:
# df = makeSummaryTable(
#     ("linear algebra", 0.13, 0.55, 7.69, 3.85, 31.27, 14.86, 25, "easy encouraging"),
#     ("calculus", 0.20, 0.45, 10.10, 5.20, 28.30, 16.40, 30, "moderate challenging"),
#     save_to_csv=True
# )
