from backend.database.db import get_connection

# Decrypting passwords during authentication
def get_student_by_email(email):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)  # Use dict cursor for key-based access
    query = """
    SELECT student_id, first_name, last_name, email, AES_DECRYPT(password, 'super_secret_key@12345!') AS password
    FROM Students
    WHERE email = %s
    """
    cursor.execute(query, (email,))
    student = cursor.fetchone()
    conn.close()
    print(student)
    if student and student['password'] is not None:
        try:
            student['password'] = student['password'].decode('utf-8')  # Try utf-8 decoding
        except UnicodeDecodeError:
            student['password'] = student['password'].decode('latin1')

    return student

def get_employee_by_email(email):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT e.employee_id, e.first_name, e.last_name, e.email, AES_DECRYPT(e.password, 'super_secret_key@12345!') AS password,
           ut.type_name AS user_type  
    FROM Employees e
    JOIN User_Types ut ON e.user_type_id = ut.user_type_id  
    WHERE e.email = %s
    """
    cursor.execute(query, (email,))
    employee = cursor.fetchone()
    print(employee)
    conn.close()
    if employee and employee['password'] is not None:
        print(employee['password'])
        try:
            employee['password'] = employee['password'].decode('utf-8')  # Try utf-8 decoding
        except UnicodeDecodeError:
            employee['password'] = employee['password'].decode('latin1')  # Fallback to latin1
    return employee

