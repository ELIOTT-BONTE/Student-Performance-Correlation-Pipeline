import pandas as pd
from datetime import datetime, timedelta
import os

# Helper Functions
def check_attendance_file_headers(attendance_file_path):
    expected_headers = [
        "Time", "User full name", "Affected user", "Event context",
        "Component", "Event name", "Description", "Origin", "IP address"
    ]
    df = pd.read_csv(attendance_file_path)
    return list(df.columns) == expected_headers

def is_holiday(date, holidays):
    for start, end in holidays:
        if start <= date <= end:
            return True
    return False

def all_weekly_sessions(ini_date, end_date, holidays=[]):
    ini_date = pd.to_datetime(ini_date)
    end_date = pd.to_datetime(end_date)
    day_of_week = ini_date.weekday()
    holidays = [(datetime.strptime(start, '%d/%m/%Y'), datetime.strptime(end, '%d/%m/%Y')) for start, end in holidays]
    sessions = []
    while ini_date <= end_date:
        if ini_date.weekday() == day_of_week and not is_holiday(ini_date, holidays):
            sessions.append(ini_date.strftime('%d/%m/%Y'))
        ini_date += timedelta(days=7)
    return sessions

def update_attendance(attendance_table, log_data, session_dates, ini_time_str, end_time_str):
    ini_time = datetime.strptime(ini_time_str, '%H:%M').time()
    end_time = datetime.strptime(end_time_str, '%H:%M').time()
    log_data['Time'] = pd.to_datetime(log_data['Time'], format='%d/%m/%y, %H:%M:%S')

    for session_date in session_dates:
        session_label = f'Session {session_date}'
        session_datetime = datetime.strptime(session_date, '%d/%m/%Y')
        ini_datetime = datetime.combine(session_datetime, ini_time)
        end_datetime = datetime.combine(session_datetime, end_time)

        present_students_ids = log_data[
            (log_data['Time'] >= ini_datetime) &
            (log_data['Time'] <= end_datetime)
        ]['User full name'].unique()

        for student_id in present_students_ids:
            if student_id in attendance_table['Student ID'].values:
                attendance_table.loc[attendance_table['Student ID'] == student_id, session_label] = 'P (2/2)'

def generate_attendance_table(course_name, worktype, schedule_path, log_data_path, holidays=[]):
    print("course_name : ", course_name)
    course_schedules = pd.read_csv(schedule_path, sep=';')
    print("Available columns:", course_schedules.columns)
    course_info = course_schedules[(course_schedules['course_name'] == course_name) & (course_schedules['worktype'] == worktype)]

    if course_info.empty:
        print("worktype : ", worktype," course name : ", course_name)

        raise ValueError("Course name or worktype not found in the schedule.")

    ini_date = course_info['ini_date'].iloc[0]
    end_date = course_info['end_date'].iloc[0]
    ini_time = course_info['ini_time'].iloc[0]
    end_time = course_info['end_time'].iloc[0]

    session_dates = all_weekly_sessions(ini_date, end_date, holidays)
    log_data = pd.read_csv(log_data_path)

    attendance_table = pd.DataFrame(columns=['Student ID'] + [f'Session {date}' for date in session_dates])
    unique_users = log_data['User full name'].unique()
    attendance_table['Student ID'] = unique_users
    attendance_table.fillna('A (0/2)', inplace=True)

    update_attendance(attendance_table, log_data, session_dates, ini_time, end_time)

    output_directory = 'pythonPrograms/output/attendance from logs table'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    updated_attendance_path = os.path.join(output_directory, 'updated_generated_attendance_table.csv')
    attendance_table.to_csv(updated_attendance_path, index=False)

    print("Attendance table has been generated and updated.")
    return updated_attendance_path


