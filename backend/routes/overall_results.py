from flask import Blueprint, request, jsonify
from backend.database.db import get_connection
from backend.routes.faculty_courses import get_employee_id_from_email

overall_results_blueprint = Blueprint('overall_results', __name__)

# Helper function to get student_id from email
def get_student_id_from_email(email):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT student_id FROM Students WHERE email = %s", (email,))
        student = cursor.fetchone()
        return student[0] if student else None
    finally:
        cursor.close()
        conn.close()

@overall_results_blueprint.route('/student/overall-results', methods=['GET'])
def get_overall_results():
    user_email = request.args.get('userEmail')
    if not user_email:
        return jsonify({"message": "Session expired. Please log in again."}), 401

    student_id = get_student_id_from_email(user_email)
    if not student_id:
        return jsonify({"message": "Student not found. Please log in again."}), 404

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT semester_id, spi, cpi FROM SPI_CPI 
            WHERE student_id = %s ORDER BY semester_id ASC
        """, (student_id,))
        results = cursor.fetchall()

        if not results:
            return jsonify({"message": "No results available"}), 404

        # Prepare data for frontend
        semesters = [{"name": f"Semester {i + 1}", "spi": result["spi"]} for i, result in enumerate(results)]
        latest_cpi = results[-1]["cpi"] if results else 0  # Get the latest CPI if available

        return jsonify({"semesters": semesters, "cpi": latest_cpi}), 200
    finally:
        cursor.close()
        conn.close()


@overall_results_blueprint.route('/faculty/grade-distribution', methods=['GET'])
def get_grade_distribution():
    user_email = request.args.get('userEmail')
    if not user_email:
        return jsonify({"message": "Session expired. Please log in again."}), 401

    employee_id = get_employee_id_from_email(user_email)
    if not employee_id:
        return jsonify({"message": "Faculty member not found. Please log in again."}), 404

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT 
                c.course_code, 
                c.course_name, 
                g.course_id, 
                sn.semester_name, 
                ay.start_year, 
                ay.end_year, 
                g.numeric_grade, 
                sg.grade AS special_grade
            FROM Grades g
            JOIN Courses c ON g.course_id = c.course_id
            JOIN Semesters s ON g.semester_id = s.semester_id
            JOIN Semester_Name sn ON s.semester_name_id = sn.semester_name_id
            JOIN Academic_Year ay ON s.academic_year_id = ay.academic_year_id
            LEFT JOIN Special_Grades sg ON g.special_grade_id = sg.special_grades_id
            WHERE g.employee_id = %s
            ORDER BY c.course_code, ay.start_year, sn.semester_name
        """, (employee_id,))

        data = cursor.fetchall()

        # Organize data by course and semester, with grade distributions
        course_data = {}
        for row in data:
            course_code = row["course_code"]
            semester_name = row["semester_name"]
            academic_year = f"{row['start_year']}-{row['end_year']}"
            course_key = (course_code, semester_name, academic_year)

            if course_key not in course_data:
                course_data[course_key] = {"course_code": course_code, "course_name": row["course_name"],
                                           "semester": semester_name, "academic_year": academic_year, "grades": {}}

            # For numeric grades, divide into bins
            if row["numeric_grade"] is not None:
                grade_bin = str(int(row["numeric_grade"] // 10 * 10)) + "-" + str(
                    int(row["numeric_grade"] // 10 * 10 + 9))
                course_data[course_key]["grades"][grade_bin] = course_data[course_key]["grades"].get(grade_bin, 0) + 1
            # For special grades, use the grade value directly
            elif row["special_grade"] is not None:
                grade = row["special_grade"]
                course_data[course_key]["grades"][grade] = course_data[course_key]["grades"].get(grade, 0) + 1

        # Convert course_data dictionary to list for JSON response
        result = [
            {
                "course_code": value["course_code"],
                "course_name": value["course_name"],
                "semester": value["semester"],
                "academic_year": value["academic_year"],
                "grades": value["grades"]
            }
            for value in course_data.values()
        ]

        return jsonify(result), 200
    finally:
        cursor.close()
        conn.close()
