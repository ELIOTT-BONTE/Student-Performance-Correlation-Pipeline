import glob
import os

def find_files_in_folder(folder_path):
    all_files = glob.glob(os.path.join(folder_path, "*.*"))
    
    # Find the grades file
    grades_files = [f for f in all_files if 'grades' in os.path.basename(f).lower()]
    
    print(f"All files found: {all_files}")
    print(f"Grades files found: {grades_files}")
    
    if not grades_files:
        raise FileNotFoundError("No grades file found in the input folder.")
    
    grades_file = grades_files[0]  # Assuming there is only one grades file

    # Find the manually tracked attendance files, exclude log files and config file
    course_files = [f for f in all_files if 'grades' not in os.path.basename(f).lower() and 'schedule' not in os.path.basename(f).lower() and 'log' not in os.path.basename(f).lower() and 'config.txt' not in os.path.basename(f).lower()]
    # Find the schedule file
    schedule_files = [f for f in all_files if 'schedule' in os.path.basename(f).lower()]
    schedule_file = schedule_files[0] if schedule_files else None
    
    # Find the log files
    log_files = [f for f in all_files if 'log' in os.path.basename(f).lower()]
    
    print(f"Course files found: {course_files}")
    print(f"Schedule file found: {schedule_file}")
    print(f"Log files found: {log_files}")
    
    return grades_file, course_files, schedule_file, log_files