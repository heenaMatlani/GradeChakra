from collections import defaultdict

def apply_course_repeat_policy(grades, grading_system, cursor):
    # Retrieve grading details and policies
    print("entered course repeat")
    course_policy = grading_system['course_and_lab_repeat']['course_repeat_policy']
    lab_policy = grading_system['course_and_lab_repeat']['lab_course_repeat_policy']
    processed_grades = []
    # Store grades by course (grouping grades by course code and handling elective changes)

    # Retrieve grading details
    grading_details = grading_system['grading_details']
    is_special_grades = grading_details['system_type'] == 'special'

    # Process each pre-grouped set of grades
    # Process each item in grades
    for entry in grades:
        # Check if entry is a list (indicating repeated or elective change grades)
        if isinstance(entry, list):
            # Apply repeat or elective change policy to grouped grades
            if len(entry)==1:
                processed_grades.append(entry[0])
            else:
                is_lab_course = any(grade.get('is_lab_course') for grade in entry)
                if is_lab_course:
                    processed_grades.append(
                        apply_repeat_policy(entry, grading_system, cursor, lab_policy, is_special_grades,))
                else:
                    processed_grades.append(
                        apply_repeat_policy(entry, grading_system, cursor, course_policy, is_special_grades))
        else:
            # Directly add non-repeated grade entries
            processed_grades.append(entry)

    return processed_grades


def apply_repeat_policy(grades, grading_system, cursor, policy, is_special_grades):
    """
    Apply the repeat policy on a group of grades for the same course.
    """
    if is_special_grades:
        # Special grading logic (when system is 'special' and uses grade points)
        special_grades_dict = {grade['special_grades_id']: grade['grade_point'] for grade in
                               grading_system['grading_details']['special_grades']}
        print(special_grades_dict)

        if policy == 'replace_with_higher_grade':
            return replace_with_higher_grade(grades, special_grades_dict)
        elif policy == 'average_of_grades':
            return average_grades(grades, special_grades_dict)
        elif policy == 'most_recent_grade':
            return most_recent_grade(grades)
    else:
        # Numeric grades logic
        if policy == 'replace_with_higher_grade':
            return replace_with_higher_grade(grades)
        elif policy == 'average_of_grades':
            return average_grades(grades)
        elif policy == 'most_recent_grade':
            return most_recent_grade(grades)


def replace_with_higher_grade(grades, special_grades_dict=None):
    """
    Replace with the highest grade from the grouped grades (special or numeric).
    """
    if special_grades_dict:
        # Handle special grades by using special_grade_id
        best_grade = max(grades, key=lambda g: special_grades_dict.get(g['special_grade_id'], 0))
    else:
        # Numeric grades logic
        best_grade = max(grades, key=lambda g: g['numeric_grade'])  # Using numeric_grade for numeric grades

    print(f"Best Grade: {best_grade}")
    return best_grade


def average_grades(grades, special_grades_dict=None):
    """
    Average the grade points of all grades in the group (special or numeric).
    """
    total_points = 0
    for grade in grades:
        if special_grades_dict:
            # Using special_grade_id to get grade points for special grades
            total_points += special_grades_dict.get(grade['special_grade_id'], 0)
        else:
            # Numeric grade points for numeric grades
            total_points += grade['numeric_grade']

    average = total_points / len(grades)

    # For numeric grades or special grades, find the closest grade to the average
    if special_grades_dict:
        best_grade = min(grades, key=lambda g: abs(special_grades_dict.get(g['special_grade_id'], 0) - average))
    else:
        best_grade = min(grades, key=lambda g: abs(g['numeric_grade'] - average))

    return best_grade


def most_recent_grade(grades):
    """
    Pick the most recent grade based on grade_id (auto-increment).
    """
    most_recent = max(grades, key=lambda g: g['grade_id'])  # Using grade_id to find the most recent
    return most_recent
