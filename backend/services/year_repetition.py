from collections import defaultdict

def apply_year_repetition_policy(grades, grading_system, cursor):
    # Retrieve grading details and year repetition rules
    print("entered year policy")
    year_repeat_policy = grading_system['year_repetition']['year_repetition_rule']
    processed_grades = []

    # Store grades by course (grouping grades by course code and handling elective changes)
    course_groups = defaultdict(list)

    for grade in grades:
        if grade.get('elective_change') == 1:
            # Group grades of both previous and new course for elective change
            course_groups[grade['previous_course_id']].append(grade)
        else:
            # Group grades based on year repeat or not
            course_groups[grade['course_id']].append(grade)

    # Now, process each group of grades
    # print(course_groups)
    for course_code, grouped_grades in course_groups.items():
        if len(grouped_grades) == 1:
            # If there's only one entry (non-repeated grade), just add it directly
            processed_grades.append(grouped_grades[0])
        else:
            # If there are multiple grades for the same course (repeated), apply the year repetition policy
            processed_grades.append(apply_year_repeat_policy(grouped_grades, grading_system, cursor, year_repeat_policy))

    return processed_grades

def apply_year_repeat_policy(grades, grading_system, cursor, policy):
    """
    Apply the year repetition policy to a group of grades for the same course.
    """
    if policy == 'reset_previous_results':
        return reset_previous_results(grades)
    elif policy == 'keep_previous_results':
        return keep_previous_results(grades)
    elif policy == 'replace_failed_courses_only':
        return replace_failed_courses_only(grades, grading_system)
    # Add other policies as needed

def reset_previous_results(grades):
    """
    Reset all grades for the year when a student repeats the year.
    This can simply mean returning an empty grade set or adjusting the grades to default values.
    """
    # Assuming grades are reset to a default or null state for all year-repeat courses
    year_repeat_grades = [grade for grade in grades if grade.get('year_repeat')]
    # print(year_repeat_grades)
    if year_repeat_grades:
        return year_repeat_grades
    return grades

def keep_previous_results(grades):
    """
    Retain grades from previous years, even if the year is repeated, and use them while calculating the result.
    Here, you can either leave the grades untouched or mark them as carried forward.
    """
    for grade in grades:
        grade['previous_grade'] = grade['grade']  # Keep a reference to previous year's grade
    return grades

def replace_failed_courses_only(grades, grading_system):
    """
    Only replace grades for courses that were failed in any previous attempts.
    If a failure exists in previous grades, return the year repeat grade if available.
    Otherwise, retain the previous grade.
    """
    passing_grade_threshold = grading_system['grading_details'].get('passing_grade_threshold', 33)  # Default threshold to 33
    special_failing_grade = grading_system['grading_details'].get('failing_grade', 'F')  # 'F' by default for special grades

    # Split grades into pre-year repeat and year repeat groups
    pre_year_repeat_grades = [grade for grade in grades if not grade.get('year_repeat')]
    year_repeat_grades = [grade for grade in grades if grade.get('year_repeat')]

    # Check if any pre-year repeat grade is a failure
    failed_in_pre_year = False
    for grade in pre_year_repeat_grades:
        if isinstance(grade['grade'], (int, float)) and grade['grade'] <= passing_grade_threshold:
            failed_in_pre_year = True
            break
        elif grade['grade'] == special_failing_grade:
            failed_in_pre_year = True
            break

    # Return the appropriate grade based on failure check and availability of year repeat grades
    if failed_in_pre_year and year_repeat_grades:
        # Failure in previous grades and year repeat grades exist, so use most recent year repeat grade
        return year_repeat_grades
    else:
        # No year repeat grades or no failure, so return the most recent pre-year repeat grade
        return pre_year_repeat_grades


