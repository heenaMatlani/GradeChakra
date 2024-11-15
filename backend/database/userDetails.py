from backend.database.db import get_connection

def get_student_details(email):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT CONCAT(s.first_name, ' ', s.last_name) AS name, s.roll_number AS rollNo, 
               b.batch_year AS batch, p.program_short_name AS program, 
               d.department_short_name AS department, s.email
        FROM Students s
        JOIN Batches b ON s.batch_id = b.batch_id
        JOIN Programs p ON b.program_id = p.program_id
        JOIN Departments d ON s.department_id = d.department_id
        WHERE s.email = %s
    """
    cursor.execute(query, (email,))
    profile = cursor.fetchone()
    conn.close()
    return profile

def get_employee_details(email):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT CONCAT(e.first_name, ' ', e.last_name) AS name, e.email, 
               d.department_short_name AS department, r.role_name AS role, DATE_FORMAT(e.start_date, '%d %b %Y') as startDate
        FROM Employees e
        JOIN Departments d ON e.department_id = d.department_id
        JOIN Roles r ON e.role_id = r.role_id
        WHERE e.email = %s
    """
    cursor.execute(query, (email,))
    profile = cursor.fetchone()
    conn.close()
    return profile
