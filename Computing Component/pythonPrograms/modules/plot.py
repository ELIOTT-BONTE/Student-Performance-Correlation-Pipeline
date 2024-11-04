import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr

def plot_correlation(csv_file_path, courseName, attendancePercentage, output_file_path):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)
    
    # Calculate studentAbsenceRate first by counting the non-numeric absence entries
    total_entries = len(df)
    absence_conditions = df[courseName].isin(["ABS_EXAM", "ABS_EXAM_JUST"])
    studentAbsenceRate = absence_conditions.sum() / total_entries * 100
    
    # Calculate studentFailRate after converting courseName to numeric, setting errors to NaN
    df[courseName] = pd.to_numeric(df[courseName], errors="coerce")
    studentFailRate = (df[courseName] < 10).sum() / total_entries * 100
    
    # Drop rows where either column has NaN
    df.dropna(subset=[courseName, attendancePercentage], inplace=True)
    
    # Group by the values to find duplicates and count them
    grouped = df.groupby([attendancePercentage, courseName]).size().reset_index(name='counts')
    
    # Calculate the correlation and its significance
    correlation, p_value = pearsonr(grouped[attendancePercentage], grouped[courseName])
    print(f"Correlation between {courseName} and {attendancePercentage}: {correlation}, p-value: {p_value}")
    
    # Fit and plot linear regression line
    slope, intercept = np.polyfit(grouped[attendancePercentage], grouped[courseName], 1)
    
    # Classify the course
    if (slope * 100) + intercept < 10:
        courseClassification1 = "hard"
    elif intercept >= 10:
        courseClassification1 = "easy"
    else:
        courseClassification1 = "fair"
        
    if slope < 0:
        courseClassification2 = "negative"
    else:
        courseClassification2 = "positive"
    
    # Plotting
    fig, ax = plt.subplots(figsize=(15, 10)) # Adjusted figure size for 2:3 aspect ratio
    scatter = ax.scatter(grouped[attendancePercentage], grouped[courseName],
                         s=grouped['counts'] * 100,
                         alpha=0.5, edgecolors='w', linewidth=0.5)
    ax.axhline(y=10, color='green', linestyle='--', linewidth=2, alpha=0.2, label='Grade = 10')
    ax.axvline(x=50, color='blue', linestyle='--', linewidth=2, alpha=0.2, label='Attendance = 50%')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 20)
    
    for i, point in grouped.iterrows():
        if point['counts'] > 1:
            ax.text(point[attendancePercentage], point[courseName],
                    str(point['counts']),
                    fontsize=9,
                    ha='center',
                    va='center')
    
    x_vals = np.array(ax.get_xlim())
    y_vals = intercept + slope * x_vals
    ax.plot(x_vals, y_vals, "--", color="red", label=f"Linear fit: y = {slope:.2f}x + {intercept:.2f}")
    ax.set_title(f"Correlation between attendance and academic achievement in {courseName}")
    ax.set_ylabel("Grade")
    ax.set_xlabel("Attendance percentage")
    ax.legend()
    ax.grid(True)
    
    # Descriptive statistics table
    descriptive_stats = df[[attendancePercentage, courseName]].describe().round(2)
    formatted_stats = descriptive_stats.applymap(lambda x: f"{x:.2f}")
    table = plt.table(cellText=formatted_stats.values,
                      colLabels=["attendance percentage", "grade"],
                      rowLabels=formatted_stats.index,
                      cellLoc='center', rowLoc='center',
                      loc='bottom', bbox=[0.2, -0.6, 0.6, 0.3]) # Adjust bbox for better fitting
    
    # Store average grade and average attendance percentage for passing it
    average_attendance_percentage = descriptive_stats.loc["mean","attendancePercentage"]
    average_grade = descriptive_stats.loc["mean", courseName]
    
    # Adjust subplot parameters to create space at the bottom for the annotations
    plt.subplots_adjust(left=0.2, right=0.8, top=0.9, bottom=0.4)
    
    # Add Pearson correlation and classification annotations below the table
    plt.figtext(0.5, 0.05, f'Pearson r: {correlation:.2f}, p-value: {p_value:.4f}, fail rate : {studentFailRate:.2f}%, absence rate: {studentAbsenceRate:.2f}%', ha='center', fontsize=12)
    plt.figtext(0.5, 0.01, f'Course Complexity : {courseClassification1}, Correlation : {courseClassification2}', ha='center', fontsize=12)
    
    # Save the plot to a file
    plt.savefig(output_file_path, bbox_inches='tight')
    print(f"Plot saved as {output_file_path}")

    # return data to create the table in main.py
    # round data to two digits
    print(round(correlation,2), round(p_value,2), round(studentFailRate,2), round(studentAbsenceRate,2), average_attendance_percentage, average_grade, (total_entries-1), courseClassification1, courseClassification2)
    print("COUNT = ", total_entries-1)
    return  round(correlation,2), round(p_value,2), round(studentFailRate,2), round(studentAbsenceRate,2), average_attendance_percentage, average_grade, (total_entries-1), courseClassification1, courseClassification2



# Example usage:
# plot_correlation("data.csv", "Grade", "AttendancePercentage", "output.png")
