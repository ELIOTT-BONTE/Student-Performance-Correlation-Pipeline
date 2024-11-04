import os

def read_config_file(config_path):
    course_info_list = []
    vacation_periods = []

    if os.path.exists(config_path):
        with open(config_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if 'vacation_periods' in line:
                    vacation_periods = eval(line.split(":")[1].strip())
                else:
                    parts = line.strip().split(', ')
                    if len(parts) == 3: # We expect 3 parts for logs analysis
                        course_name, course_abbreviation, worktype = parts
                        course_info_list.append({
                            "name": course_name,
                            "abbreviation": course_abbreviation,
                            "worktype": worktype
                        })
                    elif len(parts) == 2: # For manual attendance, user defines only 2 arguments
                        course_name, worktype = parts
                        course_info_list.append({
                            "name": course_name,
                            "abbreviation": course_name[:6],  # Default abbreviation if not specified
                            "worktype": worktype
                        })

    return course_info_list, vacation_periods