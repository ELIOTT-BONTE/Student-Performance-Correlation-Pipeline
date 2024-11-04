import pandas as pd

def cleanup(file_path, course_name):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Check if there are at least two columns to drop
    if df.shape[1] < 2:
        raise ValueError("The CSV file must have at least two columns to remove.")

    # Remove the first two columns
    df = df.iloc[:, 2:]

    # Find the index of the 'attendancePercentage' column
    try:
        index_attendance = df.columns.get_loc("attendancePercentage")
    except KeyError:
        raise KeyError("The column 'attendancePercentage' must be in the CSV.")

    # Iterate over columns after 'attendancePercentage'
    # Remove columns that do not have the header as the course name
    for col in df.columns[index_attendance + 1:]:
        if col != course_name:
            df.drop(col, axis=1, inplace=True)

    # Save the modified DataFrame back to CSV
    df.to_csv(file_path, index=False)
    print(f"CSV file has been processed and saved for course '{course_name}'.")
