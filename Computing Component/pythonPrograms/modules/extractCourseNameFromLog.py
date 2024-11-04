import os

def extract_course_name_from_log(log_file):
    base_name = os.path.basename(log_file)
    if base_name.startswith("log-"):
        return base_name[4:].rsplit('.', 1)[0]  # Remove "log-" prefix and file extension
    return base_name.rsplit('.', 1)[0]
