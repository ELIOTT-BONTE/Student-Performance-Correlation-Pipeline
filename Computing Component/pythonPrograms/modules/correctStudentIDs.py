import csv

def correct_student_IDs(attendance_file):
    with open(attendance_file, mode = "r", newline="") as file:
        reader = csv.reader(file)
        # Store modified rows
        modified_rows = []
        modified_count = 0
        for row in reader : 
            original_length = len(row[0])
            # Check if the first column's value has less than 10 digits and pad it with leading zeros
            row[0] = row[0].zfill(10)
            if len(row[0]) > original_length:
                modified_count += 1
            modified_rows.append(row)


    # Overwrite orifinal file
    with open(attendance_file, mode = "w", newline= "") as file:
        writer = csv.writer(file)
        writer.writerows(modified_rows)
        print(f"fixed student {modified_count} IDs")
        