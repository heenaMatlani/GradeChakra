from flask import Blueprint, request, jsonify
from backend.database.db import get_connection

grade_communication_blueprint = Blueprint('grade_communication', __name__)


@grade_communication_blueprint.route('/submit-grade-message', methods=['POST'])
def submit_grade_message():
    data = request.json
    user_type = data.get('userType')
    message = data.get('message')
    user_email = data.get('userEmail')

    # Check for required data
    if not message or not user_type or not user_email:
        return jsonify({'error': 'User must be logged in to submit messages'}), 401

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Fetch user ID based on user type
        if user_type == 'student':
            cursor.execute("SELECT student_id FROM Students WHERE email = %s", (user_email,))
            user_id_result = cursor.fetchone()
            if user_id_result:
                student_id = user_id_result['student_id']
                faculty_id = None
            else:
                return jsonify({'error': 'User session expired, please log in again.'}), 401

        elif user_type == 'faculty':
            cursor.execute("SELECT employee_id FROM Employees WHERE email = %s", (user_email,))
            user_id_result = cursor.fetchone()
            if user_id_result:
                faculty_id = user_id_result['employee_id']
                student_id = None
            else:
                return jsonify({'error': 'User session expired, please log in again.'}), 401
        else:
            return jsonify({'error': 'Invalid user type'}), 400

        # Insert message into IssuesRequests table
        cursor.execute("""
            INSERT INTO IssuesRequests (sender_type, student_id, faculty_id, issue_text, date_submitted, is_read)
            VALUES (%s, %s, %s, %s, CURRENT_DATE, FALSE)
        """, (user_type, student_id, faculty_id, message))

        conn.commit()
        return jsonify({'message': 'Message submitted successfully'}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()
