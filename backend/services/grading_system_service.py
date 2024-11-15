from backend.database.db import get_connection


def get_active_grading_system(batch_year):
    """
    Retrieve the active grading system for the provided batch year.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT *
        FROM Grading_System_Configuration
        WHERE start_batch_year <= %s
        AND (
            end_batch_year >= %s
            OR (end_batch_year IS NULL AND is_active = TRUE)
        )
        LIMIT 1
    """, (batch_year, batch_year))
    grading_system = cursor.fetchone()
    cursor.close()
    conn.close()
    return grading_system


def get_grading_details(grading_details_id):
    """
    Fetch grading details, including type, max score, and special grades if type is 'special'.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Grading_Details WHERE grading_details_id = %s", (grading_details_id,))
    grading_details = cursor.fetchone()
    if grading_details and grading_details["system_type"] == "special":
        cursor.execute("SELECT * FROM Special_Grades WHERE grading_details_id = %s", (grading_details_id,))
        grading_details["special_grades"] = cursor.fetchall()
    cursor.close()
    conn.close()
    return grading_details


def get_spi_cpi_rules(spi_cpi_rule_id):
    """
    Retrieve SPI/CPI calculation rules, including formula names and formulas.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.spi_name, s.cpi_name, s.round_to_decimal_places, spi.formula AS spi_formula, cpi.formula AS cpi_formula
        FROM SPI_CPI_Rules s
        JOIN SPI_Formula spi ON s.spi_formula_id = spi.spi_formula_id
        JOIN CPI_Formula cpi ON s.cpi_formula_id = cpi.cpi_formula_id
        WHERE s.spi_cpi_rule_id = %s
    """, (spi_cpi_rule_id,))
    spi_cpi_rules = cursor.fetchone()
    cursor.close()
    conn.close()
    return spi_cpi_rules


def get_year_repetition_rule_and_display(year_repetition_id, year_repetition_display_id):
    # Retrieve Year Repetition Rule
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT rule_name FROM Year_Repetition_Rules WHERE year_repeat_rule_id = %s", (year_repetition_id,))
    year_repetition_rule = cursor.fetchone()['rule_name']

    # Retrieve Year Repetition Display Option
    cursor.execute("""
        SELECT disp.option_name AS year_option_name 
        FROM Year_Repetition_Display yrd
        JOIN Display_Options disp ON yrd.display_option_id = disp.display_option_id
        WHERE yrd.year_repetition_display_id = %s
    """, (year_repetition_display_id,))
    year_repetition_display = cursor.fetchone()['year_option_name']

    cursor.close()
    conn.close()

    return {"year_repetition_rule": year_repetition_rule, "year_repetition_display": year_repetition_display}


def get_course_and_lab_course_repeat_rules(course_repeat_policy_id, lab_course_repeat_policy_id,
                                           course_repeat_and_supplementary_display_id):
    # Fetch Course Repeat Policy and Rule Name
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT grr.rule_name AS course_rule_name 
        FROM Course_Repeat_Policy crp
        JOIN Grade_Replacement_Rules grr ON crp.replacement_id = grr.replacement_id
        WHERE crp.course_repeat_policy_id = %s
    """, (course_repeat_policy_id,))
    course_repeat_policy = cursor.fetchone()['course_rule_name']

    # Fetch Lab Course Repeat Policy and Rule Name
    cursor.execute("""
        SELECT grr.rule_name AS lab_course_rule_name 
        FROM Lab_Course_Repeat_Policy lcrp
        JOIN Grade_Replacement_Rules grr ON lcrp.replacement_id = grr.replacement_id
        WHERE lcrp.lab_course_repeat_policy_id = %s
    """, (lab_course_repeat_policy_id,))
    lab_course_repeat_policy = cursor.fetchone()['lab_course_rule_name']

    # Retrieve Display Option for Course Repeat & Supplementary
    cursor.execute("""
        SELECT disp.option_name AS course_option_name 
        FROM Course_Repeat_And_Supplementary_Display crasd
        JOIN Display_Options disp ON crasd.display_option_id = disp.display_option_id
        WHERE crasd.course_repeat_and_supplementary_display_id = %s
    """, (course_repeat_and_supplementary_display_id,))
    course_repeat_and_supplementary_display = cursor.fetchone()['course_option_name']

    cursor.close()
    conn.close()

    return {
        "course_repeat_policy": course_repeat_policy,
        "lab_course_repeat_policy": lab_course_repeat_policy,
        "course_repeat_and_supplementary_display": course_repeat_and_supplementary_display
    }


def get_all_grading_details(batch_year):
    """
    Main function to retrieve all grading policies and rules for a specific batch year.
    """
    # Retrieve active grading system
    grading_system = get_active_grading_system(batch_year)
    if not grading_system:
        raise ValueError("No active grading system found for the provided batch year.")

    # Fetch grading details
    grading_details = get_grading_details(grading_system['grading_details_id'])

    # Fetch SPI/CPI rules
    spi_cpi_rules = get_spi_cpi_rules(grading_system['spi_cpi_rule_id'])

    # Fetch year repetition rules
    year_repetition = get_year_repetition_rule_and_display(grading_system['year_repetition_id'], grading_system['year_repetition_display_id'])

    # Fetch Course and Lab Course Repeat Policies and Display
    course_and_lab_repeat = get_course_and_lab_course_repeat_rules(
        grading_system['course_repeat_policy_id'],
        grading_system['lab_course_repeat_policy_id'],
        grading_system['course_repeat_and_supplementary_display_id']
    )


    # Compile all grading details
    grading_data = {
        "grading_details": grading_details,
        "spi_cpi_rules": spi_cpi_rules,
        "year_repetition": year_repetition,
        "course_and_lab_repeat": course_and_lab_repeat
    }

    return grading_data
