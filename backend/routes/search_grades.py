from flask import Blueprint, request, jsonify, send_file
from backend.database.db import get_connection
import pandas as pd
from io import BytesIO

search_grades_blueprint = Blueprint('search_grades', __name__)


@search_grades_blueprint.route('/search-grades/filter-options', methods=['GET'])
def get_filter_options():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Fetch programs, departments, and semesters for dropdowns
        cursor.execute("SELECT program_short_name AS program FROM Programs")
        programs = [row['program'] for row in cursor.fetchall()]

        cursor.execute("SELECT department_short_name AS department FROM Departments")
        departments = [row['department'] for row in cursor.fetchall()]

        cursor.execute("SELECT semester_name FROM Semester_Name")
        semesters = [row['semester_name'] for row in cursor.fetchall()]

        return jsonify({"programs": programs, "departments": departments, "semesters": semesters}), 200
    finally:
        cursor.close()
        conn.close()


@search_grades_blueprint.route('/search-grades/student/report', methods=['GET'])
def download_student_pdf():
    roll_number = request.args.get('roll_number')
    if not roll_number:
        return jsonify({"message": "Roll number is required"}), 400

    conn = get_connection()
    cursor = conn.cursor(buffered=True)
    try:
        # Get the latest student report by roll_number, ordered by semester_id descending
        cursor.execute("""
            SELECT grade_pdf 
            FROM StudentGradeReports 
            JOIN Students ON Students.student_id = StudentGradeReports.student_id 
            WHERE roll_number = %s
            ORDER BY semester_id DESC
            LIMIT 1
        """, (roll_number,))

        result = cursor.fetchone()
        if not result:
            return jsonify({"message": "No report found for this student"}), 404

        pdf_data = result[0]
        if len(pdf_data) == 0:
            return jsonify({"message": "Report data is empty"}), 404

        print(pdf_data)

        return send_file(BytesIO(pdf_data), as_attachment=True, download_name=f"{roll_number}_Report.pdf",
                         mimetype='application/pdf')
    finally:
        cursor.close()
        conn.close()


@search_grades_blueprint.route('/search-grades/batch/cpi', methods=['GET'])
def download_batch_cpi():
    batch_year = request.args.get('batch_year')
    program = request.args.get('program')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT 
                s.roll_number, 
                CONCAT(s.first_name, ' ', s.last_name) AS student_name, 
                sc.cpi
            FROM 
                Students s
            JOIN 
                SPI_CPI sc ON s.student_id = sc.student_id
            JOIN 
                Batches b ON s.batch_id = b.batch_id
            JOIN 
                Programs p ON b.program_id = p.program_id
            JOIN 
                (SELECT student_id, MAX(semester_id) AS latest_semester_id 
                 FROM SPI_CPI 
                 GROUP BY student_id) latest_sem 
                 ON sc.student_id = latest_sem.student_id 
                 AND sc.semester_id = latest_sem.latest_semester_id
            WHERE 
                b.batch_year = %s 
                AND p.program_short_name = %s
            ORDER BY 
                s.roll_number;
        """
        cursor.execute(query, (batch_year, program))
        result = cursor.fetchall()

        if not result:
            return jsonify({"message": "No data found for this batch"}), 404

        df = pd.DataFrame(result)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Batch_CPI')
        output.seek(0)
        return send_file(output, as_attachment=True, download_name=f"{program}_{batch_year}_CPI_Report.xlsx", mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    finally:
        cursor.close()
        conn.close()

@search_grades_blueprint.route('/search-grades/batch/spi_cpi', methods=['GET'])
def download_batch_spi_cpi():
    batch_year = request.args.get('batch_year')
    program = request.args.get('program')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT s.roll_number, CONCAT(s.first_name, ' ', s.last_name) AS student_name, sc.semester_id, sc.spi, sc.cpi
            FROM Students s
            JOIN SPI_CPI sc ON s.student_id = sc.student_id
            JOIN Batches b ON s.batch_id = b.batch_id
            JOIN Programs p ON b.program_id = p.program_id
            WHERE b.batch_year = %s AND p.program_short_name = %s
            ORDER BY sc.semester_id
        """
        cursor.execute(query, (batch_year, program))
        result = cursor.fetchall()

        if not result:
            return jsonify({"message": "No data found for this batch"}), 404

        df = pd.DataFrame(result)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Batch_SPI_CPI')
        output.seek(0)
        return send_file(output, as_attachment=True, download_name=f"{program}_{batch_year}_SPI_CPI_Report.xlsx", mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    finally:
        cursor.close()
        conn.close()

@search_grades_blueprint.route('/search-grades/statistics', methods=['GET'])
def calculate_statistics():
    metric = request.args.get('metric')  # 'cpi' or 'spi'
    batch_year = request.args.get('batch_year')
    program = request.args.get('program')
    department = request.args.get('department', None)
    semester = request.args.get('semester', None)
    course_code = request.args.get('course_code', None)

    if not metric:
        return jsonify({"message": "Metric (CPI or SPI) is required"}), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = f"""
            SELECT MAX(sc.{metric}) AS max_{metric}, MIN(sc.{metric}) AS min_{metric}, AVG(sc.{metric}) AS avg_{metric}
            FROM SPI_CPI sc
            JOIN Students s ON sc.student_id = s.student_id
            JOIN Batches b ON s.batch_id = b.batch_id
            JOIN Programs p ON b.program_id = p.program_id
            WHERE b.batch_year = %s AND p.program_short_name = %s
        """
        params = [batch_year, program]

        if department:
            query += " AND s.department_id = (SELECT department_id FROM Departments WHERE department_short_name = %s)"
            params.append(department)
        if semester:
            query += " AND sc.semester_id = (SELECT semester_id FROM Semesters WHERE semester_name_id = (SELECT semester_name_id FROM Semester_Name WHERE semester_name = %s))"
            params.append(semester)
        if course_code:
            query += " AND sc.course_id = (SELECT course_id FROM Courses WHERE course_code = %s)"
            params.append(course_code)

        cursor.execute(query, tuple(params))
        result = cursor.fetchone()

        if not result:
            return jsonify({"message": "No data found for the given filters"}), 404
        return jsonify(result), 200
    finally:
        cursor.close()
        conn.close()


@search_grades_blueprint.route('/search-grades/batch-department/cpi', methods=['GET'])
def download_batch_department_cpi():
    batch_year = request.args.get('batch_year')
    program = request.args.get('program')
    department = request.args.get('department')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT s.roll_number, CONCAT(s.first_name, ' ', s.last_name) AS student_name, sc.cpi
            FROM Students s
            JOIN SPI_CPI sc ON s.student_id = sc.student_id
            JOIN Batches b ON s.batch_id = b.batch_id
            JOIN Programs p ON b.program_id = p.program_id
            JOIN Departments d ON s.department_id = d.department_id
            WHERE b.batch_year = %s AND p.program_short_name = %s AND d.department_short_name = %s
        """
        cursor.execute(query, (batch_year, program, department))
        result = cursor.fetchall()

        if not result:
            return jsonify({"message": "No data found for this batch and department"}), 404

        df = pd.DataFrame(result)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Batch_Department_CPI')
        output.seek(0)
        return send_file(output, as_attachment=True, download_name=f"{program}_{batch_year}_{department}_CPI_Report.xlsx", mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    finally:
        cursor.close()
        conn.close()

@search_grades_blueprint.route('/search-grades/batch-department/spi_cpi', methods=['GET'])
def download_batch_department_spi_cpi():
    batch_year = request.args.get('batch_year')
    program = request.args.get('program')
    department = request.args.get('department')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT s.roll_number, CONCAT(s.first_name, ' ', s.last_name) AS student_name, sc.semester_id, sc.spi, sc.cpi
            FROM Students s
            JOIN SPI_CPI sc ON s.student_id = sc.student_id
            JOIN Batches b ON s.batch_id = b.batch_id
            JOIN Programs p ON b.program_id = p.program_id
            JOIN Departments d ON s.department_id = d.department_id
            WHERE b.batch_year = %s AND p.program_short_name = %s AND d.department_short_name = %s
            ORDER BY sc.semester_id
        """
        cursor.execute(query, (batch_year, program, department))
        result = cursor.fetchall()

        if not result:
            return jsonify({"message": "No data found for this batch and department"}), 404

        df = pd.DataFrame(result)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Batch_Department_SPI_CPI')
        output.seek(0)
        return send_file(output, as_attachment=True, download_name=f"{program}_{batch_year}_{department}_SPI_CPI_Report.xlsx", mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    finally:
        cursor.close()
        conn.close()

@search_grades_blueprint.route('/search-grades/grade-distribution', methods=['GET'])
def download_grade_distribution():
    semester_name = request.args.get('semester_name')
    academic_year = request.args.get('academic_year')
    batch_year = request.args.get('batch_year')
    program = request.args.get('program')
    department = request.args.get('department')
    grade_view = request.args.get('grade_view')  # 'whole' or 'course-wise'

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if grade_view == "whole":
            query = """
                SELECT sg.grade, COUNT(*) AS count
                FROM Grades g
                JOIN Special_Grades sg ON g.special_grade_id = sg.special_grades_id
                JOIN Students s ON g.student_id = s.student_id
                JOIN Batches b ON s.batch_id = b.batch_id
                JOIN Programs p ON b.program_id = p.program_id
                JOIN Semesters sem ON g.semester_id = sem.semester_id
                JOIN Academic_Year ay ON sem.academic_year_id = ay.academic_year_id
                WHERE sem.semester_name_id = (SELECT semester_name_id FROM Semester_Name WHERE semester_name = %s)
                AND ay.start_year = %s AND b.batch_year = %s AND p.program_short_name = %s AND s.department_id = (SELECT department_id FROM Departments WHERE department_short_name = %s)
                GROUP BY sg.grade
            """
            cursor.execute(query, (semester_name, academic_year, batch_year, program, department))
        else:  # course-wise
            query = """
                SELECT c.course_code, sg.grade, COUNT(*) AS count
                FROM Grades g
                JOIN Special_Grades sg ON g.special_grade_id = sg.special_grades_id
                JOIN Students s ON g.student_id = s.student_id
                JOIN Courses c ON g.course_id = c.course_id
                JOIN Batches b ON s.batch_id = b.batch_id
                JOIN Programs p ON b.program_id = p.program_id
                JOIN Semesters sem ON g.semester_id = sem.semester_id
                JOIN Academic_Year ay ON sem.academic_year_id = ay.academic_year_id
                WHERE sem.semester_name_id = (SELECT semester_name_id FROM Semester_Name WHERE semester_name = %s)
                AND ay.start_year = %s AND b.batch_year = %s AND p.program_short_name = %s AND s.department_id = (SELECT department_id FROM Departments WHERE department_short_name = %s)
                GROUP BY c.course_code, sg.grade
            """
            cursor.execute(query, (semester_name, academic_year, batch_year, program, department))

        result = cursor.fetchall()
        if not result:
            return jsonify({"message": "No data found for grade distribution"}), 404

        return jsonify(result), 200
    finally:
        cursor.close()
        conn.close()


@search_grades_blueprint.route('/search-grades/custom-query', methods=['GET'])
def execute_custom_query():
    query = request.args.get('query')
    if not query:
        return jsonify({"message": "Query parameter is required"}), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        if not result:
            return jsonify({"message": "No data found for the custom query"}), 404

        df = pd.DataFrame(result)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Custom_Query_Results')
        output.seek(0)
        return send_file(output, as_attachment=True, download_name='Custom_Query_Results.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    finally:
        cursor.close()
        conn.close()

@search_grades_blueprint.route('/search-grades/course/grades', methods=['GET'])
def download_course_grades():
    course_code = request.args.get('course_code')
    semester_name = request.args.get('semester_name')
    academic_year = request.args.get('academic_year')

    if not (course_code and semester_name and academic_year):
        return jsonify({"message": "Missing parameters"}), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT s.roll_number, CONCAT(s.first_name, ' ', s.last_name) AS student_name, c.course_code, c.course_name,
                   IF(g.numeric_grade IS NULL, sg.grade, g.numeric_grade) AS grade
            FROM Grades g
            JOIN Courses c ON g.course_id = c.course_id
            JOIN Students s ON g.student_id = s.student_id
            LEFT JOIN Special_Grades sg ON g.special_grade_id = sg.special_grades_id
            JOIN Semesters sem ON g.semester_id = sem.semester_id
            JOIN Academic_Year ay ON sem.academic_year_id = ay.academic_year_id
            WHERE c.course_code = %s AND sem.semester_name_id = (SELECT semester_name_id FROM Semester_Name WHERE semester_name = %s) 
            AND ay.start_year = %s
        """
        cursor.execute(query, (course_code, semester_name, academic_year))
        result = cursor.fetchall()

        if not result:
            return jsonify({"message": "No data found for this course and semester"}), 404

        df = pd.DataFrame(result)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Course_Grades')
        output.seek(0)
        return send_file(output, as_attachment=True, download_name=f"{course_code}_{semester_name}_{academic_year}_Grades.xlsx", mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    finally:
        cursor.close()
        conn.close()

