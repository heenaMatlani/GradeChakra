import zipfile
from io import BytesIO
from flask import Blueprint, request, jsonify
from backend.database.db import get_connection
import os
from backend.services.pdf_data_collector import get_student_data
import pandas as pd

pdf_handling_blueprint = Blueprint('pdf_handling', __name__)


@pdf_handling_blueprint.route('/upload-zip', methods=['POST'])
def upload_zip():
    """Handle the uploaded ZIP file with PDFs named by roll number and semester."""
    if 'zipFile' not in request.files:
        return jsonify({"error": "No ZIP file provided."}), 400

    zip_file = request.files['zipFile']
    try:
        # Open a connection to the database
        connection = get_connection()
        cursor = connection.cursor()

        with zipfile.ZipFile(BytesIO(zip_file.read()), 'r') as zip_ref:
            for pdf_path in zip_ref.namelist():
                pdf_filename = os.path.basename(pdf_path)
                print(pdf_filename)
                if not pdf_filename.endswith('.pdf'):
                    continue

                # Extract roll_number and semester number from filename
                file_parts = pdf_filename.split('_')
                if len(file_parts) != 2 or not file_parts[1].endswith('.pdf'):
                    continue

                roll_number = file_parts[0]
                semester_number = int(file_parts[1].replace('.pdf', ''))

                # Fetch student_id based on roll_number
                cursor.execute("SELECT student_id FROM Students WHERE roll_number = %s", (roll_number,))
                student_id_row = cursor.fetchone()
                print(roll_number)
                if not student_id_row:
                    continue  # Skip if student is not found
                student_id = student_id_row[0]
                print(student_id)
                # Fetch distinct semester_ids for this student and sort them
                cursor.execute("SELECT DISTINCT semester_id FROM Grades WHERE student_id = %s ORDER BY semester_id ASC",
                               (student_id,))
                sorted_semester_ids = [row[0] for row in cursor.fetchall()]
                print(sorted_semester_ids)

                # Map semester_number to corresponding semester_id
                if semester_number - 1 < len(sorted_semester_ids):
                    semester_id = sorted_semester_ids[semester_number - 1]
                else:
                    continue  # Skip if semester_number is out of range
                print(roll_number, student_id, semester_number, semester_id)
                # Read PDF file data
                pdf_data = zip_ref.read(pdf_path)
                print(pdf_data)
                # Store PDF in StudentGradeReports table
                cursor.execute("""
                    INSERT INTO StudentGradeReports (student_id, semester_id, grade_pdf)
                    VALUES (%s, %s, %s)
                    """, (student_id, semester_id, pdf_data))

        # Commit the transaction to save all entries
        connection.commit()
        return jsonify({"message": "ZIP file processed and PDFs uploaded successfully."})
    except Exception as e:
        connection.rollback()
        return jsonify({"error": f"Failed to process ZIP file: {str(e)}"}), 500
    finally:
        cursor.close()
        connection.close()


@pdf_handling_blueprint.route('/generate-pdfs', methods=['POST'])
def generate_pdfs():
    # Retrieve the uploaded zip file from the request
    if 'zip_file' not in request.files:
        return jsonify({'error': 'No zip file provided'}), 400

    zip_file = request.files['zip_file']

    try:
        # Call the function to extract roll numbers from the zip file
        roll_numbers = extract_roll_numbers(zip_file)

        # Return extracted roll numbers or proceed with PDF generation
        # Here, we just return the roll numbers for demonstration
        print(roll_numbers)
        for roll_no in roll_numbers:
            data = get_student_data(roll_no)
            print(data)


    except Exception as e:
        print("Error extracting roll numbers:", e)
        return jsonify({'error': 'Failed to process zip file'}), 500


def extract_roll_numbers(zip_file):
    roll_numbers = []

    # Open the zip file in memory
    with zipfile.ZipFile(BytesIO(zip_file.read()), 'r') as z:
        for file_name in z.namelist():
            # Extract and read each Excel file
            with z.open(file_name) as excel_file:
                # Assuming roll numbers are in a specific column, like "Roll Number"
                df = pd.read_excel(excel_file)

                # Check if 'Roll Number' column exists
                if 'Roll Number' in df.columns:
                    roll_numbers.extend(df['Roll Number'].tolist())
                else:
                    print(f"Roll Number column not found in {file_name}")

    return roll_numbers