from flask import Blueprint, request, jsonify
from backend.database.authentication import get_student_by_email, get_employee_by_email
from backend.utils.jwt_auth import generate_token

login_blueprint = Blueprint('login', __name__)

USER_TYPE_MAPPING = {
    'Admin': 'admin',
    'Faculty': 'faculty',
    'Academic Staff': 'staff'
}

@login_blueprint.route('/login', methods=['POST'])
def login():

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user_type = data.get('user_type')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    # Check for student or employee login
    if user_type == 'student':
        user = get_student_by_email(email)
        user_type_to_return = 'student'
    else:
        user = get_employee_by_email(email)
        if user:
            # Map the user type to the specified output
            user_type_to_return = USER_TYPE_MAPPING.get(user['user_type'], user['user_type'])  # Default to original if not found
        else:
            user_type_to_return = None    # Check if user exists and password matches
    if user and user['password'] == password:
        token = generate_token(user['email'])
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'userName': f"{user['first_name']} {user['last_name']}",
            'userRole': user_type_to_return  # Send 'student' for students or user_type (admin, faculty, etc.) for employees
        }), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

