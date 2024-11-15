from backend.database.db import get_connection

def get_logs():
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT l.log_id, CONCAT(e.first_name, ' ', e.last_name) AS employee_name, a.action_type, l.description as comment, l.timestamp
        FROM Logs l
        JOIN Employees e ON l.employee_id = e.employee_id
        JOIN Actions a ON l.action_id = a.action_id
        ORDER BY l.timestamp DESC;
        """
        cursor.execute(query)
        logs = cursor.fetchall()

        return logs

    except Exception as e:
        print(f"Error fetching logs: {e}")
        return []

    finally:
        cursor.close()
        connection.close()
