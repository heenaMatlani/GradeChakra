from flask import Blueprint, request, jsonify
from backend.database.db import get_connection

messages_blueprint = Blueprint('messages', __name__)

@messages_blueprint.route('/messages', methods=['GET'])
def get_messages():
    msg_type = request.args.get('type')
    unread_only = request.args.get('unreadOnly') == 'true'
    read_only = request.args.get('readOnly') == 'true'
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')
    page = request.args.get('page', type=int, default=1)
    page_size = request.args.get('pageSize', type=int, default=10)

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Base query
    query = """
        SELECT ir.request_id, ir.issue_text, ir.date_submitted, ir.is_read,
               CASE WHEN ir.sender_type = 'student' THEN CONCAT(s.first_name, ' ', s.last_name) ELSE CONCAT(e.first_name, ' ', e.last_name)  END AS name,
               CASE WHEN ir.sender_type = 'student' THEN s.email ELSE e.email END AS email
        FROM IssuesRequests ir
        LEFT JOIN Students s ON ir.student_id = s.student_id
        LEFT JOIN Employees e ON ir.faculty_id = e.employee_id
        WHERE ir.sender_type = %s
    """
    params = [msg_type]

    # Apply filters
    if unread_only:
        query += " AND ir.is_read = FALSE"
    elif read_only:
        query += " AND ir.is_read = TRUE"
    if start_date:
        query += " AND date_submitted >= %s"
        params.append(start_date)
    if end_date:
        query += " AND date_submitted <= %s"
        params.append(end_date)

    # Apply pagination
    query += " ORDER BY date_submitted DESC LIMIT %s OFFSET %s"
    params.extend([page_size, (page - 1) * page_size])
    cursor.execute(query, params)
    messages = cursor.fetchall()

    # Fetch total count for pagination
    total_count_query = """
        SELECT COUNT(*) AS total
        FROM IssuesRequests ir
        WHERE ir.sender_type = %s
    """
    total_count_params = [msg_type]

    # Include read/unread filters in the total count query
    if unread_only:
        total_count_query += " AND ir.is_read = FALSE"
    elif read_only:
        total_count_query += " AND ir.is_read = TRUE"

    if start_date:
        total_count_query += " AND ir.date_submitted >= %s"
        total_count_params.append(start_date)
    if end_date:
        total_count_query += " AND ir.date_submitted <= %s"
        total_count_params.append(end_date)
    cursor.execute(total_count_query, total_count_params)
    total_messages = cursor.fetchone()['total']
    total_pages = (total_messages + page_size - 1) // page_size if total_messages % page_size != 0 else total_messages // page_size
    conn.close()
    return jsonify({"messages": messages, "totalPages": total_pages})

@messages_blueprint.route('/messages/<int:message_id>/mark-read', methods=['PUT'])
def mark_message_as_read(message_id):
    return toggle_message_read_state(message_id, True)

@messages_blueprint.route('/messages/<int:message_id>/mark-unread', methods=['PUT'])
def mark_message_as_unread(message_id):
    return toggle_message_read_state(message_id, False)

def toggle_message_read_state(message_id, is_read):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE IssuesRequests SET is_read = %s WHERE request_id = %s", (is_read, message_id))
        conn.commit()
        status = "read" if is_read else "unread"
        return jsonify({"message": f"Message marked as {status}"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
