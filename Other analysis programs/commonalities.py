import pandas as pd

# Load the provided ODS file
file_path = '/mnt/data/all courses labels.ods'
data = pd.read_excel(file_path, engine='odf')

# Split the dataset into three clusters based on the 'Attendance cluster' column
low_attendance = data[data['Attendance cluster'] == 'Low']
moderate_attendance = data[data['Attendance cluster'] == 'Moderate']
high_attendance = data[data['Attendance cluster'] == 'High']

# Define a function to find the most represented characteristic for each column in a cluster
def most_represented_characteristic(cluster):
    result = []
    for column in cluster.columns:
        if column not in ['Course', 'Name', 'Attendance cluster']:
            characteristic_counts = cluster[column].value_counts(dropna=True)
            if not characteristic_counts.empty:
                most_rep = characteristic_counts.idxmax()
                count = characteristic_counts.max()
                total_non_nan = characteristic_counts.sum()
                percentage = (count / total_non_nan) * 100
                result.append([column, most_rep, count, percentage, total_non_nan])
    return pd.DataFrame(result, columns=['Characteristic', 'Most Represented', 'Count', 'Percentage', 'Total'])

# Find the most represented characteristic for each cluster
low_attendance_result = most_represented_characteristic(low_attendance)
moderate_attendance_result = most_represented_characteristic(moderate_attendance)
high_attendance_result = most_represented_characteristic(high_attendance)

import ace_tools as tools; tools.display_dataframe_to_user(name="Low Attendance Cluster Characteristics", dataframe=low_attendance_result)
tools.display_dataframe_to_user(name="Moderate Attendance Cluster Characteristics", dataframe=moderate_attendance_result)
tools.display_dataframe_to_user(name="High Attendance Cluster Characteristics", dataframe=high_attendance_result)

(low_attendance_result.head(), moderate_attendance_result.head(), high_attendance_result.head())
