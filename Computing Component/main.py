import sys
import os
import pandas as pd
from flask import Flask, request, redirect, url_for, send_from_directory, render_template, send_file
import zipfile
import io
import shutil

# Include dependencies in the path
module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'pythonPrograms'))
if module_path not in sys.path:
    sys.path.insert(0, module_path)

from pipeline import pipeline
from modules.makeSummaryTable import makeSummaryTable
from modules.findFilesInFolder import find_files_in_folder
from modules.readConfigFile import read_config_file
from modules.extractCourseNameFromLog import extract_course_name_from_log

app = Flask(__name__)
UPLOAD_FOLDER = 'input'
OUTPUT_FOLDER = 'output'
DOWNLOAD_FOLDER = 'download'
ZIP_FILENAME = 'output_files.zip'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['ZIP_FILENAME'] = ZIP_FILENAME

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    # Clear the input and output directory
    for f in os.listdir(app.config['UPLOAD_FOLDER']):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], f))

    # Clear the output directory
    for filename in os.listdir(app.config['OUTPUT_FOLDER']):
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

    if 'files[]' not in request.files:
        return redirect(request.url)
    files = request.files.getlist('files[]')
    for file in files:
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('process_files'))

@app.route('/process')
def process_files():
    courses = []
    input_folder = app.config['UPLOAD_FOLDER']
    config_path = os.path.join(input_folder, "config.txt")
    course_infos, vacation_periods = read_config_file(config_path)

    grades_file, course_files, schedule_file, log_files = find_files_in_folder(input_folder)

    if course_files:
        for course_info in course_infos:
            course_name = course_info["name"]
            worktype = course_info["worktype"]
            course_abbreviation = course_info.get("abbreviation", course_name[:6])  # default to first 6 chars if not found
            
            # Process manual attendance files
            for course_file in course_files:
                if course_name == os.path.splitext(os.path.basename(course_file))[0]:
                    correlation, p_value, fail_rate, abs_rate, attendance_mean, grade_mean, student_count, classification1, classification2 = pipeline(course_file, grades_file, course_name, worktype=worktype)
                    courseClass = classification1 + " " + classification2
                    courses.append((course_name,worktype, correlation, p_value, fail_rate, abs_rate, attendance_mean, grade_mean, student_count,  courseClass))
        
        # Process log files
        for log_file in log_files:
            course_name_from_log = extract_course_name_from_log(log_file)
            for course_info in course_infos:
                if course_info["name"] == course_name_from_log:
                    course_abbreviation = course_info.get("abbreviation", course_name_from_log[:6])
                    worktype = course_info["worktype"]
                    correlation, p_value, fail_rate, abs_rate, attendance_mean, grade_mean, student_count, classification1, classification2 = pipeline(
                        None, grades_file, course_name_from_log, worktype=worktype, courseAbreviation=course_abbreviation, schedulePath=schedule_file, logPath=log_file, holidays=vacation_periods
                    )
                    courseClass = classification1 + " " + classification2
                    courses.append((course_name_from_log,worktype, correlation, p_value, fail_rate, abs_rate, attendance_mean, grade_mean, student_count, courseClass))

    csv_output_file = os.path.join(app.config['OUTPUT_FOLDER'], 'Summary.csv')
    png_output_file = os.path.join(app.config['OUTPUT_FOLDER'], 'Summary.png')
    makeSummaryTable(*courses, csv_filename=csv_output_file, png_filename=png_output_file)

    # Create a zip file of the output directory
    zip_output_file = os.path.join(app.config['OUTPUT_FOLDER'], app.config['ZIP_FILENAME'])
    with zipfile.ZipFile(zip_output_file, 'w') as zipf:
        for root, dirs, files in os.walk(app.config['OUTPUT_FOLDER']):
            for file in files:
                if file != app.config['ZIP_FILENAME']:  # Skip the zip file itself
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), app.config['OUTPUT_FOLDER']))

    return redirect(url_for('download_file', filename=app.config['ZIP_FILENAME']))

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)

@app.route('/download/instructions')
def download_instructions():
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], 'instructions/Read_those_instructions.txt', as_attachment=True)

@app.route('/download/example')
def download_example():
    memory_file = io.BytesIO()
    example_folder = os.path.join(app.config['DOWNLOAD_FOLDER'], 'example')
    with zipfile.ZipFile(memory_file, 'w') as zf:
        for root, dirs, files in os.walk(example_folder):
            for file in files:
                zf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), example_folder))
    memory_file.seek(0)
    return send_file(memory_file, download_name='example.zip', as_attachment=True)

@app.route('/health')
def health_check():
    return "Health Check OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
