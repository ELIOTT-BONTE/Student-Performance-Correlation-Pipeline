# files are stored to the output folder in between two pipeline components

# assumptions : the attendance file is an excel file
# a "Student ID" column exists in the attendance file
# each session is represented by a separate column
# a present student is noted "y", "A (2/2)" or "x"
# an absent student is noted "" or "E (0/2)"

# the grades file respects the standard format

import pandas as pd
from modules.convertToCSV import file_to_csv
from modules.convertSymbols import convert_symbols
from modules.dropEmptyColumns import delete_empty_columns
from modules.computePresencePercentage import compute_sessions_attended
from modules.gradesPreprocess import preprocess_grades
from modules.innerJoin import join_csv_files
from modules.plot import plot_correlation
from modules.correctStudentIDs import correct_student_IDs
from makeTableFromLogs import generate_attendance_table
from modules.createFolder import create_folder_if_not_exists
from modules.cleanup import cleanup

def pipeline(attendance_file=None, grades_file=None, courseName="", worktype=None, courseAbreviation=None, schedulePath=None, logPath=None, holidays=None):

    if attendance_file:
        # Convert the attendance Excel file to CSV
        attendance_working_file = "pythonPrograms/output/attendance_file.csv"
        file_to_csv(attendance_file, attendance_working_file)
    else:
        # Generate attendance table from logs
        if not all([worktype, courseAbreviation, schedulePath, logPath, holidays]):
            raise ValueError("If attendance_file is not provided, all parameters for log processing must be provided.")
        generate_attendance_table(courseAbreviation, worktype, schedulePath, logPath, holidays)
        attendance_working_file = "pythonPrograms/output/attendance from logs table/updated_generated_attendance_table.csv"

    # Drop empty columns
    delete_empty_columns(attendance_working_file)

    # Correct student IDs
    correct_student_IDs(attendance_working_file)

    # Convert symbols in the attendance file
    convert_symbols(attendance_working_file)

    # Compute presence percentage
    compute_sessions_attended(attendance_working_file)

    # Preprocess grades file
    grades_working_file = "pythonPrograms/output/grades_file.csv"
    file_to_csv(grades_file, grades_working_file)
    preprocess_grades(grades_working_file)

    #Create output folder for this course
    create_folder_if_not_exists(f"output/{courseName}")

    # Perform inner join on Student IDs of attendance and grades files
    joined_file = f"output/{courseName}/{courseName + ' ' + worktype}.csv"
    join_csv_files(attendance_working_file, grades_working_file, joined_file)

    # Remove extra information relating to other courses from joined table
    cleanup(f"output/{courseName}/{courseName + ' ' + worktype}.csv", courseName)



    # Plot attendance percentage vs grade correlation
    plot_file = f"pythonPrograms/output/plots/{courseName}.png"
    plot_file = f"output/{courseName}/{courseName + ' ' + worktype}.png"
    correlation, p_value, fail_rate, abs_rate, attendance_mean, grade_mean, student_count, classification1, classification2 = plot_correlation(joined_file, courseName, "attendancePercentage", plot_file)

    return correlation, p_value, fail_rate, abs_rate, attendance_mean, grade_mean, student_count, classification1, classification2


