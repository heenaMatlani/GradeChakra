from flask import Blueprint, jsonify
from backend.database.getLogs import get_logs

logs_blueprint = Blueprint('view_logs', __name__)

@logs_blueprint.route('/logs', methods=['GET'])
def view_logs():
    logs = get_logs()
    return jsonify(logs), 200
