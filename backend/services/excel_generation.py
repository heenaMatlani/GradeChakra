import pandas as pd
from collections import defaultdict
from io import BytesIO
from backend.database.db import get_connection


def group_students_by_batch_program_department(roll_numbers, cursor):
    # Create a defaultdict to hold grouped data
    grouped_data = defaultdict(list)

    try:
        for roll_number in roll_numbers:
            # Fetch the batch year, program, department, and student name for the student using the roll number
            cursor.execute("""
                SELECT b.batch_year, p.program_short_name, d.department_short_name, CONCAT(s.first_name, ' ', s.last_name) AS name
                FROM Students s
                JOIN Batches b ON s.batch_id = b.batch_id
                JOIN Programs p ON b.program_id = p.program_id
                JOIN Departments d ON s.department_id = d.department_id
                WHERE s.roll_number = %s
            """, (roll_number,))

            student_data = cursor.fetchone()

            if student_data:
                batch_year, program, department, name = student_data

                # Grouping by (batch_year, program, department)
                grouped_data[(batch_year, program, department)].append({
                    'roll_number': roll_number,
                    'batch_year': batch_year,
                    'program': program,
                    'department': department,
                    'name': name
                })

        return grouped_data

    except Exception as e:
        print(f"Error grouping students: {e}")
        return None


def get_student_grades(student_id, cursor):
    # Get all grades for a student
    cursor.execute("""
        SELECT g.course_id, c.course_code, c.course_name, c.credits, g.numeric_grade, g.special_grade_id
        FROM Grades g
        JOIN Courses c ON g.course_id = c.course_id
        WHERE g.student_id = %s
        ORDER BY g.semester_id
    """, (student_id,))
    return cursor.fetchall()

def get_student_spi_cpi(student_id, cursor):
    cursor.execute("""
        SELECT semester_id, spi, cpi
        FROM SPI_CPI
        WHERE student_id = %s
        ORDER BY semester_id
    """, (student_id,))
    return cursor.fetchall()


def generate_excel_reports(roll_numbers):
    connection = get_connection()
    cursor = connection.cursor()
    grouped_data = group_students_by_batch_program_department(roll_numbers, cursor)

    excel_files = []

    try:
        for group_key, students in grouped_data.items():
            batch_year, program, department = group_key
            # Prepare data structure for the Excel sheet
            all_data = []
            all_headers = set()  # To ensure course codes are unique across the sheet
            headers = ['Roll Number', 'Student Name', 'Batch Year', 'Program', 'Department']
            is_first_student = True
            for student in students:
                student_id = get_student_id(student['roll_number'], cursor)  # Fetch student_id using roll_number
                grades = get_student_grades(student_id, cursor)
                spi_cpi_records = get_student_spi_cpi(student_id, cursor)

                # Prepare headers dynamically
                course_data = {}
                repeat_counts = defaultdict(int)

                for grade in grades:
                    course_id, course_code, course_name, credits, numeric_grade, special_grade_id = grade
                    repeat_counts[course_code] += 1
                    course_header = f"{course_code}" + ("_repeat" * (repeat_counts[course_code] - 1))

                    # Handle special grades
                    grade_value = get_special_grade_value(special_grade_id, cursor) if special_grade_id else numeric_grade
                    grade_name = get_special_grade_name(special_grade_id, cursor) if special_grade_id else None

                    # If the course code is already in the header, add _repeat for the repeated course
                    # Add course columns to headers if it's not already included
                    if course_header not in all_headers:
                        all_headers.add(course_header)
                        if not special_grade_id:
                            headers.extend([f"{course_header}", f"{course_name}", f"{course_header}_credits", f"{course_header}_grade_value"])
                        else:
                            headers.extend([f"{course_header}", f"{course_name}", f"{course_header}_credits", f"{course_header}_grade_value", f"{course_header}_grade_name"])

                    course_data[course_header] = [course_code, course_name, credits, grade_value]
                    if grade_name:
                        course_data[course_header].append(grade_name)

                if is_first_student:
                    # Add SPI/CPI headers based on the number of semesters
                    for idx, record in enumerate(spi_cpi_records, 1):
                        headers.append(f"Sem_{idx}_SPI")
                        headers.append(f"Sem_{idx}_CPI")
                    headers.append("Overall_CPI")
                    is_first_student = False



                # Add student data row
                row_data = [student['roll_number'], student['name'], batch_year, program, department]
                for course_code in all_headers:
                    if course_code in course_data:
                        row_data.extend(course_data[course_code])
                    else:
                        row_data.extend([None, None, None, None])
                        if grade_name:
                            row_data.extend([None])

                for spi_cpi in spi_cpi_records:
                    row_data.append(spi_cpi[1])  # SPI
                    row_data.append(spi_cpi[2])  # CPI

                # Overall CPI as the last CPI of the latest semester
                overall_cpi = spi_cpi_records[-1][2] if spi_cpi_records else None
                row_data.append(overall_cpi)
                all_data.append(row_data)

            # Create a DataFrame for the group and save it to an Excel file in memory

            df = pd.DataFrame(all_data, columns=headers)
            file_name = f"{batch_year}_{program}_{department}_report.xlsx"

            # Write the Excel file to a BytesIO object
            excel_io = BytesIO()
            df.to_excel(excel_io, index=False)
            excel_io.seek(0)

            excel_files.append({
                'filename': file_name,
                'file': excel_io
            })

    except Exception as e:
        print(f"Error generating Excel report: {e}")

    finally:
        cursor.close()
        connection.close()

    return excel_files


def get_student_id(roll_number, cursor):
    cursor.execute("""
        SELECT student_id FROM Students WHERE roll_number = %s
    """, (roll_number,))
    student_id = cursor.fetchone()
    return student_id[0] if student_id else None


def get_special_grade_name(special_grade_id, cursor):
    cursor.execute("""
        SELECT grade FROM Special_Grades WHERE special_grades_id = %s
    """, (special_grade_id,))
    special_grade = cursor.fetchone()
    return special_grade[0] if special_grade else None

def get_special_grade_value(special_grade_id, cursor):
    cursor.execute("""
        SELECT grade_point FROM Special_Grades WHERE special_grades_id = %s
    """, (special_grade_id,))
    special_grade = cursor.fetchone()
    return special_grade[0] if special_grade else None