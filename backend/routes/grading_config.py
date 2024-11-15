import re

from flask import Blueprint, request, jsonify
from backend.database.db import get_connection

grading_config_blueprint = Blueprint('grading_config', __name__)

@grading_config_blueprint.route('/set-grading-rules', methods=['POST'])
def set_grading_rules():
    data = request.json
    print(data)
    try:
        grading_system = data.get("grading_system")
        year_repetition = data.get("year_repetition")
        course_repeat = data.get("course_repeat")
        lab_course_repeat = data.get("lab_course_repeat")
        course_repeat_and_supplementary_display_rule = data.get("course_repeat_and_supplementary_display")
        spi_formula = data.get("spi_formula")
        spi_name = data.get("spi_name")
        cpi_name = data.get("cpi_name")
        start_batch_year = data.get("start_batch_year")
        round_to_decimal_places = data.get("round_to_decimal_places", 2)  # Default to 2 if not provided

        use_best_n_of_m = grading_system.get("use_best_n_of_m", None)

        # Initialize variables for best_n and total_m
        best_n = None
        total_m = None

        # If "use_best_n_of_m" exists, parse the format "use_best_X_of_Y"
        if use_best_n_of_m:
            match = re.match(r"^use_best_(\d+)_of_(\d+)$", use_best_n_of_m)
            if match:
                best_n = int(match.group(1))
                total_m = int(match.group(2))
                use_best_n_of_m_bool = True
                # Check if best_n < total_m
                if best_n >= total_m:
                    return jsonify({'error': "'best_n' must be less than 'total_m' in 'use_best_n_of_m'."}), 400
            else:
                return jsonify({'error': "Invalid 'use_best_n_of_m' format. Expected 'use_best_X_of_Y'."}), 400
        else:
            use_best_n_of_m_bool = False

        # Connect to DB
        conn = get_connection()
        cursor = conn.cursor()

        # 1. Insert or update Grading Details
        cursor.execute("""
            INSERT INTO Grading_Details (system_type, max_score, use_best_n_of_m, best_n, total_m)
            VALUES (%s, %s, %s, %s, %s)
        """, (grading_system['type'], grading_system['max_score'], use_best_n_of_m_bool, best_n, total_m))
        grading_details_id = cursor.lastrowid  # Get the last inserted id

        # 2. Insert Special Grades if grading type is 'special'
        if grading_system['type'] == 'special':
            for grade, point in grading_system['grades'].items():
                cursor.execute("""
                    INSERT INTO Special_Grades (grade, grade_point, grading_details_id)
                    VALUES (%s, %s, %s)
                """, (grade, point, grading_details_id))

        # 3. Set Year Repetition Rules
        cursor.execute("SELECT year_repeat_rule_id FROM Year_Repetition_Rules WHERE rule_name = %s", (year_repetition['rule'],))
        year_repetition_id = cursor.fetchone()[0]

        # 4. Set Display Options for Year Repetition
        cursor.execute("SELECT display_option_id FROM Display_Options WHERE option_name = %s", (year_repetition['display'],))
        year_repetition_display = cursor.fetchone()[0]

        cursor.execute("SELECT year_repetition_display_id FROM Year_Repetition_Display WHERE display_option_id = %s", (year_repetition_display,))
        year_repetition_display_db = cursor.fetchone()
        if year_repetition_display_db:
            year_repetition_display_id = year_repetition_display_db[0]
        else:
            cursor.execute("INSERT INTO Year_Repetition_Display (display_option_id) VALUES (%s)", (year_repetition_display,))
            year_repetition_display_id = cursor.lastrowid

        # 5. Set Course Repeat Policy by fetching or creating policy
        cursor.execute("SELECT replacement_id FROM Grade_Replacement_Rules WHERE rule_name = %s", (course_repeat,))
        course_repeat_replacement_id = cursor.fetchone()[0]

        cursor.execute("SELECT course_repeat_policy_id FROM Course_Repeat_Policy WHERE replacement_id = %s", (course_repeat_replacement_id,))
        course_repeat_policy = cursor.fetchone()
        if course_repeat_policy:
            course_repeat_policy_id = course_repeat_policy[0]
        else:
            cursor.execute("INSERT INTO Course_Repeat_Policy (replacement_id) VALUES (%s)", (course_repeat_replacement_id,))
            course_repeat_policy_id = cursor.lastrowid

        # 6. Set Lab Course Repeat Policy by fetching or creating policy
        cursor.execute("SELECT replacement_id FROM Grade_Replacement_Rules WHERE rule_name = %s", (lab_course_repeat,))
        lab_course_repeat_replacement_id = cursor.fetchone()[0]

        cursor.execute("SELECT lab_course_repeat_policy_id FROM Lab_Course_Repeat_Policy WHERE replacement_id = %s", (lab_course_repeat_replacement_id,))
        lab_course_repeat_policy = cursor.fetchone()
        if lab_course_repeat_policy:
            lab_course_repeat_policy_id = lab_course_repeat_policy[0]
        else:
            cursor.execute("INSERT INTO Lab_Course_Repeat_Policy (replacement_id) VALUES (%s)", (lab_course_repeat_replacement_id,))
            lab_course_repeat_policy_id = cursor.lastrowid

        # 7. Set Course Repeat & Supplementary Display Option
        cursor.execute("SELECT display_option_id FROM Display_Options WHERE option_name = %s", (course_repeat_and_supplementary_display_rule,))
        course_repeat_and_supplementary_display = cursor.fetchone()[0]

        cursor.execute("SELECT course_repeat_and_supplementary_display_id FROM Course_Repeat_And_Supplementary_Display WHERE display_option_id = %s", (course_repeat_and_supplementary_display,))
        course_repeat_and_supplementary_display_db = cursor.fetchone()
        print(course_repeat_and_supplementary_display_db)
        if course_repeat_and_supplementary_display_db:
            course_repeat_and_supplementary_display_id = course_repeat_and_supplementary_display_db[0]
        else:
            cursor.execute("INSERT INTO Course_Repeat_And_Supplementary_Display (display_option_id) VALUES (%s)", (course_repeat_and_supplementary_display,))
            course_repeat_and_supplementary_display_id = cursor.lastrowid


        cursor.execute("SELECT spi_formula_id FROM SPI_Formula WHERE formula_name = %s", (spi_formula,))
        spi_formula_row = cursor.fetchone()
        if not spi_formula_row:
            return jsonify(
                {'error': "SPI formula not found. Please insert it into SPI_Formula table."}), 400
        spi_formula_id = spi_formula_row[0]

        # Get CPI formula ID
        cursor.execute("SELECT cpi_formula_id FROM CPI_Formula WHERE formula_name = %s", ('default_cpi_formula',))
        cpi_formula_row = cursor.fetchone()
        if not cpi_formula_row:
            return jsonify(
                {'error': "CPI formula not found. Please insert it into CPI_Formula table."}), 400
        cpi_formula_id = cpi_formula_row[0]

        # Insert into SPI_CPI_Rules, referencing the formula IDs
        cursor.execute("""
            SELECT spi_cpi_rule_id FROM SPI_CPI_Rules WHERE spi_formula_id = %s AND cpi_formula_id = %s AND spi_name = %s AND cpi_name = %s AND round_to_decimal_places = %s
        """, (spi_formula_id, cpi_formula_id, spi_name, cpi_name, round_to_decimal_places))
        existing_spi_cpi_rule = cursor.fetchone()

        if existing_spi_cpi_rule:
            # If SPI_CPI Rule already exists, use the existing id
            spi_cpi_rule_id = existing_spi_cpi_rule[0]
        else:
            # Insert new SPI_CPI Rule
            cursor.execute("""
                INSERT INTO SPI_CPI_Rules (spi_formula_id, cpi_formula_id, spi_name, cpi_name, round_to_decimal_places)
                VALUES (%s, %s, %s, %s, %s)
            """, (spi_formula_id, cpi_formula_id, spi_name, cpi_name, round_to_decimal_places))
            spi_cpi_rule_id = cursor.lastrowid

        # 9. Insert the Grading System Configuration
        cursor.execute("UPDATE Grading_System_Configuration SET is_active = false")

        cursor.execute("""
            INSERT INTO Grading_System_Configuration (
                grading_details_id, year_repetition_id, course_repeat_policy_id, lab_course_repeat_policy_id,
                year_repetition_display_id, course_repeat_and_supplementary_display_id, spi_cpi_rule_id, start_batch_year, is_active
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            grading_details_id, year_repetition_id, course_repeat_policy_id, lab_course_repeat_policy_id,
            year_repetition_display_id, course_repeat_and_supplementary_display_id, spi_cpi_rule_id, start_batch_year, True
        ))

        conn.commit()
        return jsonify({'message': 'Grading rules set successfully'}), 201

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@grading_config_blueprint.route('/fetch-rules', methods=['GET'])
def fetch_rules():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch all rules and descriptions
        cursor.execute("SELECT rule_name, description FROM Year_Repetition_Rules")
        year_repetition_rules = cursor.fetchall()

        cursor.execute("SELECT rule_name, description FROM Grade_Replacement_Rules")
        course_repeat_rules = cursor.fetchall()

        cursor.execute("SELECT option_name, description FROM Display_Options")
        display_options = cursor.fetchall()

        cursor.execute("SELECT formula_name FROM SPI_Formula")
        spi_formulas = cursor.fetchall()

        conn.close()

        return jsonify({
            "year_repetition_rules": year_repetition_rules,
            "course_repeat_rules": course_repeat_rules,
            "display_options": display_options,
            "spi_formulas": spi_formulas
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
