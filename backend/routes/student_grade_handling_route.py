from flask import Blueprint, request, jsonify, send_file
from io import BytesIO
from backend.database.db import get_connection
from backend.services.pdf_data_collector import get_student_data
from backend.services.pdkMaker import get_student_pdf

grade_reports_blueprint = Blueprint('grade_reports', __name__)

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

@grade_reports_blueprint.route('/student/grade-reports', methods=['GET'])
def get_student_reports():
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
            SELECT DISTINCT semester_id FROM Grades 
            WHERE student_id = %s ORDER BY semester_id ASC
        """, (student_id,))
        reports = cursor.fetchall()

        if not reports:
            return jsonify({"message": "No results available"}), 404

        semester_reports = [{"semester": f"Semester {i + 1}", "semester_id": report["semester_id"]}
                            for i, report in enumerate(reports)]
        return jsonify(semester_reports), 200
    finally:
        cursor.close()
        conn.close()

@grade_reports_blueprint.route('/download-grade-pdf', methods=['GET'])
def download_grade_pdf():
    user_email = request.args.get('userEmail')
    semester_id = request.args.get('semesterId')

    if not user_email or not semester_id:
        return jsonify({"message": "Session expired. Please log in again."}), 401

    student_id = get_student_id_from_email(user_email)
    if not student_id:
        return jsonify({"message": "Student not found. Please log in again."}), 404

    conn = get_connection()
    cursor = conn.cursor()
    try:
        pdf_data = get_student_data(student_id, semester_id)
        pdf_io = get_student_pdf(pdf_data)

        cursor.execute("SELECT roll_number FROM Students WHERE student_id = %s", (student_id,))
        roll_no = cursor.fetchone()

        return send_file(pdf_io, as_attachment=True, download_name=f"{roll_no[0]}_Semester_{semester_id}.pdf", mimetype='application/pdf')

    finally:
        cursor.close()
        conn.close()
