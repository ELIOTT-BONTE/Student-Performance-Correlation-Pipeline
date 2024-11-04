import pandas as pd
from datetime import datetime, timedelta, time

def all_weekly_sessions(start_date, end_date, day_of_week):
    """Generate all session dates between start_date and end_date that fall on the specified day_of_week."""
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    day_generator = (start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1))
    return [day.strftime('%d/%m/%Y') for day in day_generator if day.weekday() == day_of_week]


# User inputs
start_session_date = '2023-09-23' # First session date
end_session_date = '2023-12-16'  # Last session date
day_of_week = 3 # Thursday (0=Monday, 6=Sunday)
attendance_table_path = 'generated_attendance_table.csv'
log_data_path = 'data/bics/logs-moodle/2023-2024-ws/sem-1/anon_logs_F1_BAINFOR-7_20240104-2239.csv'

# Load the CSV files
attendance_table = pd.read_csv(attendance_table_path)
log_data = pd.read_csv(log_data_path)

# Convert 'Time' column in log_data to datetime objects
log_data['Time'] = pd.to_datetime(log_data['Time'], format='%d/%m/%y, %H:%M:%S')

# Calculate all session Fridays between the start and end dates
session_dates = all_weekly_sessions(start_session_date, end_session_date, day_of_week)

# Filter log data for activities on Fridays between 10:00 and 12:00
filtered_log_data = log_data[
    (log_data['Time'].dt.dayofweek == day_of_week) & # 4 represents Friday
    (log_data['Time'].dt.time >= time(10, 0)) &
    (log_data['Time'].dt.time <= time(12, 0))
]

# Update attendance for each student based on session dates
for session_date in session_dates:
    session_label = f'Session {session_date}' # Adjust based on your table format
    present_students_ids = filtered_log_data[
        filtered_log_data['Time'].dt.strftime('%d/%m/%Y') == session_date
    ]['User full name'].unique()

    for student_id in present_students_ids:
        if student_id in attendance_table['Student ID'].values:
            print("student found")
            attendance_table.loc[attendance_table['Student ID'] == student_id, session_label] = 'P (2/2)'

# Save the updated attendance table
updated_attendance_path = 'updated_generated_attendance_table.csv'
attendance_table.to_csv(updated_attendance_path, index=False)

print("Attendance records updated.")
