from backend.database.db import get_connection
from backend.services.grade_replacement import apply_course_repeat_policy
from backend.services.year_repetition import apply_year_repetition_policy
from collections import defaultdict
import numpy as np

def process_student_grades(student_id, grading_system):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        print("entered processing")
        # Fetch grades and courses for the student
        cursor.execute("SELECT * FROM Grades WHERE student_id = %s ORDER BY semester_id ASC", (student_id,))
        columns = [col[0] for col in cursor.description]
        # Fetch all rows and convert each row to a dictionary
        grades = [dict(zip(columns, row)) for row in cursor.fetchall()]
        # print(grades)
        # Apply year repetition and course repeat policies
        print("entered year policy")
        processed_grades = apply_year_repetition_policy(grades, grading_system, cursor)
        print(processed_grades, "1")
        final_grades = apply_course_repeat_policy(processed_grades, grading_system, cursor)
        print("222\n",final_grades)
        # Group grades by semester ID in ascending order
        semester_grades = defaultdict(list)
        for grade in final_grades:
            semester_grades[grade['semester_id']].append(grade)

        # Fetch CPI formula from database
        cursor.execute("SELECT formula FROM CPI_Formula WHERE formula_name = 'default_cpi_formula'")
        cpi_formula = cursor.fetchone()[0]
        # Initialize cumulative values for CPI calculation
        cumulative_credits = []
        cumulative_grade_values = []
        all_semester_spi_cpi = []  # To store results of each semester's SPI and cumulative CPI

        # Calculate SPI and cumulative CPI for each semester
        spi_formula = grading_system['spi_cpi_rules']['spi_formula']  # SPI formula from grading system
        for semester_id, grades_in_semester in sorted(semester_grades.items()):
            # Calculate SPI for the semester
            print("calculating spi")
            spi = calculate_spi(semester_id, grades_in_semester, spi_formula, cursor, grading_system)
            all_semester_spi_cpi.append((semester_id, spi))

            # Accumulate course credits and grade values for CPI calculation
            for grade in grades_in_semester:
                cursor.execute("SELECT credits FROM Courses WHERE course_id = %s", (grade['course_id'],))
                course_credit = cursor.fetchone()[0]
                cumulative_credits.append(course_credit)

                if grading_system['grading_details']['system_type'] == 'special':
                    cursor.execute("SELECT grade_point FROM Special_Grades WHERE special_grades_id = %s", (grade['special_grade_id'],))
                    grade_value = cursor.fetchone()[0]
                else:
                    grade_value = grade['numeric_grade']

                cumulative_grade_values.append(grade_value)

            # Calculate cumulative CPI up to the current semester
            print("calculating cpi")
            cpi = calculate_cpi(cumulative_credits, cumulative_grade_values, cpi_formula, grading_system)

            # Check for existing SPI/CPI for this semester and student
            cursor.execute("""
                SELECT spi, cpi FROM SPI_CPI WHERE student_id = %s AND semester_id = %s
            """, (student_id, semester_id))
            existing_spi_cpi = cursor.fetchone()

            # Insert or update SPI and CPI only if they have changed
            if not existing_spi_cpi or existing_spi_cpi[0] != spi or existing_spi_cpi[1] != cpi:
                cursor.execute("""
                    INSERT INTO SPI_CPI (student_id, semester_id, spi, cpi)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE spi = VALUES(spi), cpi = VALUES(cpi)
                """, (student_id, semester_id, spi, cpi))

        print(all_semester_spi_cpi)

        conn.commit()
        return {"student_id": student_id, "spi_cpi": all_semester_spi_cpi, "status": "calculated successfully"}

    except Exception as e:
        conn.rollback()
        return {"error": str(e)}

    finally:
        cursor.close()
        conn.close()


def calculate_spi(semester_id, grades, spi_formula, cursor, grading_system):
    # Retrieve credits and grade values to calculate SPI
    course_credits = []
    grade_values = []

    for grade in grades:
        cursor.execute("SELECT credits FROM Courses WHERE course_id = %s", (grade['course_id'],))
        course_credit = cursor.fetchone()[0]
        course_credits.append(course_credit)
        if grading_system['grading_details']['system_type'] == 'special':
            cursor.execute("SELECT grade_point FROM Special_Grades WHERE special_grades_id = %s", (grade['special_grade_id'],))
            grade_value = cursor.fetchone()[0]
        else:
            grade_value = grade['numeric_grade']

        grade_values.append(grade_value)

    # Calculate SPI using the formula

    spi = eval(spi_formula, {"np": np, "semester_course_credits": course_credits, "semester_grade_value": grade_values})
    spi = round(spi, grading_system['spi_cpi_rules']['round_to_decimal_places'])
    return spi


def calculate_cpi(cumulative_credits, cumulative_grade_values, cpi_formula, grading_system):
    # Calculate CPI using the formula with cumulative credits and grade values
    cpi = eval(cpi_formula, {"np": np, "total_course_credits": cumulative_credits, "grade_value": cumulative_grade_values})
    cpi = round(cpi, grading_system['spi_cpi_rules']['round_to_decimal_places'])
    return cpi
