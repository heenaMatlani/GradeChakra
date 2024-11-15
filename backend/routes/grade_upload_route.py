from flask import Blueprint, request, jsonify, send_file
from backend.services.handle_grade_upload import handle_grade_upload
import pandas as pd
import io
import zipfile
from io import BytesIO
from backend.services.excel_generation import generate_excel_reports

grade_upload_blueprint = Blueprint('grade_upload', __name__)

@grade_upload_blueprint.route('/upload-grades', methods=['POST'])
def upload_grades():
    if 'excelFile' in request.files:
        file = request.files['excelFile']
        data = pd.read_excel(file)
        grades_uploaded = data.to_dict(orient='records')
    elif request.is_json:
        data = request.get_json()
        grades_uploaded = data.get("grades")
    else:
        return jsonify({"error": "No valid data provided"}), 400

    # Process grades data
    result = handle_grade_upload(grades_uploaded)

    if "error" in result:
        return jsonify(result), 400

    # excel_files = generate_excel_reports(result[1])
    #
    # if excel_files:
    #     # Create an in-memory zip file
    #     zip_buffer = BytesIO()
    #
    #     with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
    #         for file in excel_files:
    #             # The file object that contains the excel data
    #             file_data = file['file']
    #             file_name = file['filename']
    #             zip_file.writestr(file_name, file_data.read())  # Write each file to the zip
    #
    #     zip_buffer.seek(0)  # Rewind the buffer to the beginning
    return jsonify({"message": "Grades processed and Submitted Successfully!"}), 200

