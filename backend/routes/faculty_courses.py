from flask import Blueprint, request, jsonify, send_file
from backend.database.db import get_connection
import pandas as pd
from io import BytesIO

faculty_courses_blueprint = Blueprint('faculty_courses', __name__)

# Helper function to get employee_id from email
def get_employee_id_from_email(email):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT employee_id FROM Employees WHERE email = %s", (email,))
        employee = cursor.fetchone()
        return employee[0] if employee else None
    finally:
        cursor.close()
        conn.close()

@faculty_courses_blueprint.route('/faculty/courses', methods=['GET'])
def get_faculty_courses():
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
            SELECT DISTINCT g.course_id, g.semester_id, c.course_code, c.course_name,
                   sn.semester_name, ay.start_year, ay.end_year
            FROM Grades g
            JOIN Courses c ON g.course_id = c.course_id
            JOIN Semesters s ON g.semester_id = s.semester_id
            JOIN Semester_Name sn ON s.semester_name_id = sn.semester_name_id
            JOIN Academic_Year ay ON s.academic_year_id = ay.academic_year_id
            WHERE g.employee_id = %s
            ORDER BY ay.start_year, sn.semester_name
        """, (employee_id,))
        courses = cursor.fetchall()

        # Structure the data for frontend with `course_id` and `semester_id`
        course_list = [
            {
                "code": course["course_code"],
                "description": course["course_name"],
                "semester": course["semester_name"],
                "academic_year": f"{course['start_year']}-{course['end_year']}",
                "course_id": course["course_id"],
                "semester_id": course["semester_id"]
            }
            for course in courses
        ]

        return jsonify(course_list), 200
    finally:
        cursor.close()
        conn.close()



@faculty_courses_blueprint.route('/faculty/filter-options', methods=['GET'])
def get_filter_options():
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
            SELECT DISTINCT c.course_code, sn.semester_name
            FROM Grades g
            JOIN Courses c ON g.course_id = c.course_id
            JOIN Semesters s ON g.semester_id = s.semester_id
            JOIN Semester_Name sn ON s.semester_name_id = sn.semester_name_id
            WHERE g.employee_id = %s
        """, (employee_id,))
        data = cursor.fetchall()

        # Extract unique course codes and semester names
        course_codes = list(set([item['course_code'] for item in data]))
        semesters = list(set([item['semester_name'] for item in data]))

        return jsonify({"course_codes": course_codes, "semesters": semesters}), 200
    finally:
        cursor.close()
        conn.close()


@faculty_courses_blueprint.route('/faculty/course-grades', methods=['GET'])
def get_course_grades():
    course_id = request.args.get('course_id')
    semester_id = request.args.get('semester_id')
    academic_year = request.args.get('academic_year')
    download = request.args.get('download', 'false').lower() == 'true'

    if not (course_id and semester_id and academic_year):
        return jsonify({"message": "Missing parameters"}), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = """
            SELECT
                c.course_code,
                c.course_name,
                sn.semester_name,
                ay.start_year AS academic_year,
                s.roll_number,
                CONCAT(s.first_name, ' ', s.last_name) AS student_name,
                IF(g.numeric_grade IS NULL, sg.grade, g.numeric_grade) AS grade,
                gt.type_name AS grade_type
            FROM Grades g
            JOIN Courses c ON g.course_id = c.course_id
            JOIN Semesters sem ON g.semester_id = sem.semester_id
            JOIN Academic_Year ay ON sem.academic_year_id = ay.academic_year_id
            JOIN Semester_Name sn ON sem.semester_name_id = sn.semester_name_id
            JOIN Students s ON g.student_id = s.student_id
            LEFT JOIN Special_Grades sg ON g.special_grade_id = sg.special_grades_id
            JOIN Grade_Types gt ON g.grade_type_id = gt.grade_type_id
            WHERE g.course_id = %s AND g.semester_id = %s AND ay.start_year = %s
        """
        cursor.execute(query, (course_id, semester_id, academic_year))
        rows = cursor.fetchall()

        if not rows:
            return jsonify({"message": "No data found for this course and semester"}), 404

        if download:
            print("Hi")
            df = pd.DataFrame(rows)
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Grades')
            output.seek(0)

            return send_file(output, as_attachment=True,
                             download_name=f"{rows[0]['course_code']}_{rows[0]['semester_name']}_{rows[0]['academic_year']}.xlsx",
                             mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        else:
            return jsonify({"grades": rows}), 200

    finally:
        cursor.close()
        conn.close()



@faculty_courses_blueprint.route('/faculty/courses-expanded', methods=['GET'])
def get_faculty_courses_expanded():
    user_email = request.args.get('userEmail')
    if not user_email:
        return jsonify({"message": "Session expired. Please log in again."}), 401

    employee_id = get_employee_id_from_email(user_email)
    if not employee_id:
        return jsonify({"message": "Faculty member not found. Please log in again."}), 404

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Query to fetch courses taught by the faculty member, ordered lexicographically by course code and chronologically by semester
        cursor.execute("""
            SELECT c.course_code, c.course_name, g.course_id, s.semester_id, sn.semester_name, 
                   ay.start_year, ay.end_year
            FROM Grades g
            JOIN Courses c ON g.course_id = c.course_id
            JOIN Semesters s ON g.semester_id = s.semester_id
            JOIN Semester_Name sn ON s.semester_name_id = sn.semester_name_id
            JOIN Academic_Year ay ON s.academic_year_id = ay.academic_year_id
            WHERE g.employee_id = %s
            ORDER BY c.course_code, ay.start_year, sn.semester_name
        """, (employee_id,))

        data = cursor.fetchall()

        # Structure data to group by course
        courses_dict = {}
        for item in data:
            course_code = item['course_code']
            if course_code not in courses_dict:
                courses_dict[course_code] = {
                    "course_id": item["course_id"],
                    "code": course_code,
                    "name": item["course_name"],
                    "semesters": []
                }
            # Append semester data for each course
            courses_dict[course_code]["semesters"].append({
                "semester_id": item["semester_id"],
                "semester": item["semester_name"],
                "academic_year": f"{item['start_year']}-{item['end_year']}"
            })

        # Convert courses_dict to a list for the frontend
        courses_list = list(courses_dict.values())

        return jsonify(courses_list), 200
    finally:
        cursor.close()
        conn.close()
