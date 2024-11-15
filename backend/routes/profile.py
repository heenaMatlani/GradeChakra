import mysql
from flask import Blueprint, jsonify, request

from backend.database.authentication import get_student_by_email, get_employee_by_email
from backend.database.db import get_connection
from backend.utils.jwt_auth import decode_token
from backend.database.userDetails import get_student_details, get_employee_details

profile_blueprint = Blueprint('profile', __name__)


@profile_blueprint.route('/profile', methods=['GET'])
def get_profile():
    # Get the Bearer token from the headers
    token = request.headers.get('Authorization').split(" ")[1]  # Bearer <token>

    # Verify the token to check for authenticity, but we will use email from the request params
    decoded_email = decode_token(token)
    if not decoded_email:
        return jsonify({'message': 'Invalid token'}), 401

    # Fetch user_type and email from request params
    user_type = request.args.get('user_type')
    user_email = request.args.get('email')  # Email is sent explicitly in the request params
    # Fetch the profile based on user type
    if user_type == 'student':
        profile = get_student_details(user_email)
    else:
        profile = get_employee_details(user_email)

    # Check if profile exists and return the appropriate response
    if profile:
        return jsonify(profile), 200
    else:
        return jsonify({'message': 'Profile not found'}), 404

@profile_blueprint.route('/change-password', methods=['POST'])
def change_password():
    token = request.headers.get('Authorization').split(" ")[1]
    decoded_email = decode_token(token)
    if not decoded_email:
        return jsonify({'message': 'Invalid token'}), 401

    data = request.json
    old_password = data.get('oldPassword')
    new_password = data.get('newPassword')

    # Check if the user is a student or an employee
    user_type = data.get('userType')
    user_email = data.get('userEmail')
    if user_type == 'student':
        user = get_student_by_email(user_email)
    else:
        user = get_employee_by_email(user_email)

    # Directly compare the passwords without decode
    if not user or user['password'] != old_password:
        return jsonify({'message': 'Old password is incorrect'}), 403

    try:
        # Encrypt the new password
        conn = get_connection()
        cursor = conn.cursor()
        if user_type == 'student':
            query = """
            UPDATE Students SET password = %s
            WHERE email = %s
            """
        else:
            query = """
            UPDATE Employees SET password = %s
            WHERE email = %s
            """

        cursor.execute(query, (new_password, user_email))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Password changed successfully'}), 200
    except mysql.connector.Error as e:
        print(f"Error updating password: {e}")
        return jsonify({'message': 'Failed to change password'}), 500

