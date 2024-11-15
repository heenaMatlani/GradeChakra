import math

from backend.database.db import get_connection
from backend.services.grading_system_service import get_all_grading_details
from backend.services.calculate_spi_cpi import process_student_grades

def handle_grade_upload(grades_uploaded):
    conn = get_connection()
    cursor = conn.cursor()
    roll_numbers = set()
    try:
        for grade in grades_uploaded:
            # Unpack grade data
            roll_number = grade.get("roll_number")
            roll_numbers.add(roll_number)
            course_code = grade.get("course_code")
            grade_value = grade.get("grade")
            grade_type = grade.get("grade_type")
            semester_name = grade.get("semester")
            academic_year = grade.get("academic_year")
            elective_change = grade.get("elective_change", "no")
            new_course_code = grade.get("new_course_code", None)
            previous_course_id = grade.get("previous_course_id", None)
            employee_id = grade.get("employee_id")
            # 1. Ensure Course Exists
            course_id = get_course(course_code, cursor)
            print("course done")
            # 2. Ensure Semester Exists
            semester_id = get_or_create_semester(semester_name, academic_year, cursor)
            print("sem done")
            # 3. Ensure Grade Type Exists
            grade_type_id = get_grade_type(grade_type, cursor)
            print("grade done")

            # 4. Insert or update grade data in Grades table
            insert_grade(roll_number, course_id, semester_id, employee_id, grade_value, grade_type_id, elective_change,
                         new_course_code, previous_course_id, cursor)
        print("inserted")
        conn.commit()
        for roll_number in roll_numbers:
            # Fetch student data including batch year
            cursor.execute("""
                SELECT s.student_id, b.batch_year 
                FROM Students s
                JOIN Batches b ON s.batch_id = b.batch_id
                WHERE s.roll_number = %s
            """, (roll_number,))
            student = cursor.fetchone()

            if not student:
                raise ValueError(f"Student with roll number {roll_number} not found.")

            student_id, batch_year = student
            print("grading system fetching")
            # Step 3: Fetch the active grading system for the student's batch year
            grading_system = get_all_grading_details(batch_year)
            print("grading system fetched")
            # Step 4: Calculate SPI and CPI for the student based on their grading system
            print("processing data")
            process_student_grades(student_id, grading_system)
            print("processing done")

            # Commit all changes after processing

        return {"message": "Grades processed and inserted successfully"}, roll_numbers

    except Exception as e:
        print(e)
        conn.rollback()
        return {"error": str(e)}

    finally:
        cursor.close()
        conn.close()


def get_course(course_code, cursor):
    cursor.execute("SELECT course_id FROM Courses WHERE course_code = %s", (course_code,))
    course = cursor.fetchone()

    return course[0]


def get_or_create_semester(semester_name, academic_year, cursor):
    # Ensure Semester_Name exists
    cursor.execute("SELECT semester_name_id FROM Semester_Name WHERE semester_name = %s", (semester_name,))
    semester_name_id = cursor.fetchone()
    if semester_name_id:
        semester_name_id = semester_name_id[0]
    if not semester_name_id:
        cursor.execute("INSERT INTO Semester_Name (semester_name) VALUES (%s)", (semester_name,))
        semester_name_id = cursor.lastrowid

    # Ensure Academic Year exists
    cursor.execute("SELECT academic_year_id FROM Academic_Year WHERE start_year = %s",
                   (academic_year,))
    academic_year_id = cursor.fetchone()
    if academic_year_id:  # If the academic year exists, unpack the value
        academic_year_id = academic_year_id[0]
    if not academic_year_id:
        cursor.execute("INSERT INTO Academic_Year (start_year, end_year) VALUES (%s, %s)", (academic_year,academic_year+1))
        academic_year_id = cursor.lastrowid

    # Ensure Semester record exists
    cursor.execute("""
        SELECT semester_id FROM Semesters WHERE semester_name_id = %s AND academic_year_id = %s
    """, (semester_name_id, academic_year_id))
    semester = cursor.fetchone()
    if semester:
        return semester[0]
    else:
        cursor.execute("""
            INSERT INTO Semesters (semester_name_id, academic_year_id, start_month, end_month)
            VALUES (%s, %s, %s, %s)
        """, (semester_name_id, academic_year_id, "August", "December"))  # Default months
        return cursor.lastrowid


def get_grade_type(grade_type, cursor):
    cursor.execute("SELECT grade_type_id FROM Grade_Types WHERE type_name = %s", (grade_type,))
    result = cursor.fetchone()

    return result[0]


def insert_grade(roll_number, course_id, semester_id, college_employee_id, grade_value, grade_type_id, elective_change, new_course_code,
                 previous_course_id, cursor):
    # Fetch the student_id and batch_id based on the roll_number
    cursor.execute("""
        SELECT s.student_id, b.batch_year 
        FROM Students s
        JOIN Batches b ON s.batch_id = b.batch_id
        WHERE s.roll_number = %s
    """, (roll_number,))
    student = cursor.fetchone()

    if not student:
        raise ValueError(f"Student with roll number {roll_number} not found.")

    student_id, batch_year = student
    print("Student ID fetched:", student_id)
    print("Batch Year fetched:", batch_year)

    # Convert elective_change to boolean
    elective_change_bool = elective_change.lower() == 'yes'
    # Fetch the employee_id based on college_employee_id
    cursor.execute("""
        SELECT employee_id FROM Employees WHERE college_employee_id = %s
    """, (college_employee_id,))
    employee = cursor.fetchone()

    if not employee:
        raise ValueError(f"Employee with college_employee_id {college_employee_id} not found.")

    employee_id = employee[0]
    print("Employee ID fetched:", employee_id)
    # Check if the grade is alphabetical or numeric
    if grade_value.isalpha():  # Alphabetical grade
        # Search for the special grade in the Special_Grades table
        cursor.execute("SELECT special_grades_id FROM Special_Grades WHERE grade = %s", (grade_value,))
        special_grade = cursor.fetchone()

        if special_grade:
            special_grade_id = special_grade[0]
            numeric_grade = None  # No numeric grade for special grades
        else:
            raise ValueError(f"Special grade '{grade_value}' not found in the Special_Grades table.")
        cursor.fetchall()
    else:  # Numeric grade
        special_grade_id = None
        try:
            numeric_grade = float(grade_value)  # Convert the numeric grade value to float
            if numeric_grade != numeric_grade:  # Check for NaN
                raise ValueError(f"Invalid numeric grade value: '{grade_value}'")
        except ValueError:
            raise ValueError(f"Invalid numeric grade value: '{grade_value}'")

    print("inserting ss")
    if isinstance(new_course_code, float) and math.isnan(new_course_code):
        new_course_code = None
    if isinstance(previous_course_id, float) and math.isnan(previous_course_id):
        previous_course_id = None
    print(        student_id, course_id, semester_id, numeric_grade, grade_type_id, elective_change_bool, new_course_code,
        previous_course_id, special_grade_id, employee_id)
    # Insert into Grades table, now including employee_id and handling special/numeric grades
    cursor.execute("""
        INSERT INTO Grades (student_id, course_id, semester_id, numeric_grade, grade_type_id, elective_change, new_course_id, previous_course_id, special_grade_id, employee_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        student_id, course_id, semester_id, numeric_grade, grade_type_id, elective_change_bool, new_course_code,
        previous_course_id, special_grade_id, employee_id
    ))


