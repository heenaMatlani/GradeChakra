from backend.database.db import get_connection

def get_student_data(student_id, semester_id):
    data = {}
    semester_id = int(semester_id)

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Get basic student info
        cursor.execute("""
            SELECT 
                CONCAT(s.first_name, ' ', s.last_name) AS Name,
                p.program_full_name AS Program_Name,
                s.roll_number AS Roll_Number,
                b.batch_year AS Batch_Year,
                d.department_full_name AS Department_Name,
                p.total_semesters AS Total_Semesters,
                CURDATE() AS Date
            FROM Students s
            JOIN Batches b ON s.batch_id = b.batch_id
            JOIN Programs p ON b.program_id = p.program_id
            JOIN Departments d ON s.department_id = d.department_id
            WHERE s.student_id = %s
        """, (student_id,))

        student_info = cursor.fetchone()
        if not student_info:
            return {"error": f"No data found for student ID {student_id}"}

        data.update(student_info)
        data['semesters'] = []

        # Get all semester IDs and map them to logical semester numbers
        cursor.execute("""
            SELECT DISTINCT sm.semester_id
            FROM Semesters sm
            JOIN Grades g ON sm.semester_id = g.semester_id
            WHERE g.student_id = %s
            ORDER BY sm.semester_id
        """, (student_id,))

        semester_ids = [row['semester_id'] for row in cursor.fetchall()]
        semester_id_map = {sem_id: i + 1 for i, sem_id in enumerate(sorted(semester_ids))}

        # Validate and filter based on the provided semester_id
        if semester_id not in semester_id_map.values():
            return {"error": f"Invalid semester ID {semester_id} for student ID {student_id}"}

        max_semester_logical = semester_id
        valid_semester_ids = [sem_id for sem_id, sem_num in semester_id_map.items() if sem_num <= max_semester_logical]

        # Query for semester details and courses
        if len(valid_semester_ids) == 1:
            query = """
                SELECT 
                    sm.semester_id AS Semester_Id,
                    ay.start_year AS Acad_Start,
                    ay.end_year AS Acad_End,
                    sm.start_month AS Semester_Start,
                    sm.end_month AS Semester_End,
                    g.course_id, 
                    c.course_name AS Course_Name,
                    c.course_code AS Course_Code,
                    c.credits AS Course_Credit,
                    g.numeric_grade AS Course_Grade,
                    g.special_grade_id AS Special_Grade_ID
                FROM Semesters sm
                JOIN Grades g ON sm.semester_id = g.semester_id
                JOIN Courses c ON g.course_id = c.course_id
                JOIN Academic_Year ay ON sm.academic_year_id = ay.academic_year_id
                WHERE g.student_id = %s AND sm.semester_id = %s
                ORDER BY sm.semester_id
            """
            params = (student_id, valid_semester_ids[0])
        else:
            query = """
                SELECT 
                    sm.semester_id AS Semester_Id,
                    ay.start_year AS Acad_Start,
                    ay.end_year AS Acad_End,
                    sm.start_month AS Semester_Start,
                    sm.end_month AS Semester_End,
                    g.course_id, 
                    c.course_name AS Course_Name,
                    c.course_code AS Course_Code,
                    c.credits AS Course_Credit,
                    g.numeric_grade AS Course_Grade,
                    g.special_grade_id AS Special_Grade_ID
                FROM Semesters sm
                JOIN Grades g ON sm.semester_id = g.semester_id
                JOIN Courses c ON g.course_id = c.course_id
                JOIN Academic_Year ay ON sm.academic_year_id = ay.academic_year_id
                WHERE g.student_id = %s AND sm.semester_id IN %s
                ORDER BY sm.semester_id
            """
            params = (student_id, tuple(valid_semester_ids))

        cursor.execute(query, params)

        current_semester = None
        for row in cursor.fetchall():
            db_semester_id = row['Semester_Id']
            logical_semester_number = semester_id_map[db_semester_id]

            if current_semester != logical_semester_number:
                current_semester = logical_semester_number
                semester_data = {
                    "Semester_Start": row['Semester_Start'],
                    "Acad_Start": row['Acad_Start'],
                    "Semester_End": row['Semester_End'],
                    "Acad_End": row['Acad_End'],
                    "courses": []
                }
                data['semesters'].append(semester_data)

            # Handle special grades
            if row['Special_Grade_ID']:
                cursor.execute("""
                    SELECT grade AS Course_Grade
                    FROM Special_Grades
                    WHERE special_grades_id = %s
                """, (row['Special_Grade_ID'],))
                course_grade = cursor.fetchone()['Course_Grade']
            else:
                course_grade = row['Course_Grade']

            course_data = {
                "Course_Name": row['Course_Name'],
                "Course_Code": row['Course_Code'],
                "Course_Credit": row['Course_Credit'],
                "Course_Grade": course_grade
            }
            data['semesters'][-1]['courses'].append(course_data)

        # Get SPI and CPI details
        if len(valid_semester_ids) == 1:
            cursor.execute("""
                SELECT 
                    sc.spi AS Semester_SPI,
                    sc.cpi AS Semester_CPI,
                    sm.semester_id AS Semester_Id
                FROM SPI_CPI sc
                JOIN Semesters sm ON sc.semester_id = sm.semester_id
                WHERE sc.student_id = %s AND sm.semester_id = %s
                ORDER BY sm.semester_id
            """, (student_id, valid_semester_ids[0]))
        else:
            cursor.execute("""
                SELECT 
                    sc.spi AS Semester_SPI,
                    sc.cpi AS Semester_CPI,
                    sm.semester_id AS Semester_Id
                FROM SPI_CPI sc
                JOIN Semesters sm ON sc.semester_id = sm.semester_id
                WHERE sc.student_id = %s AND sm.semester_id IN %s
                ORDER BY sm.semester_id
            """, (student_id, tuple(valid_semester_ids)))

        data["SPI_Name"] = "S.P.I"
        data["CPI_Name"] = "C.P.I"
        spi_cpi_data = cursor.fetchall()
        data["SPI_CPI"] = {}

        # Add SPI and CPI values to the data
        for i, entry in enumerate(spi_cpi_data, start=1):
            data["SPI_CPI"][f"Sem_{i}_spi"] = entry["Semester_SPI"]
            data["SPI_CPI"][f"Sem_{i}_cpi"] = entry["Semester_CPI"]

        total_semesters = student_info['Total_Semesters']
        if len(spi_cpi_data) == total_semesters:
            data['is_completed'] = "COMPLETE"
        else:
            data['is_completed'] = "INCOMPLETE"

        return data

    except Exception as e:
        return {"error": str(e)}

    finally:
        cursor.close()
        conn.close()
