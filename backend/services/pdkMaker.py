from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from datetime import datetime
from decimal import Decimal
from io import BytesIO

# # Sample data as provided
# data = {
#     'Name': 'Heena Matlani',
#     'Program_Name': 'Bachelor of Technology',
#     'Roll_Number': 'B202001001',
#     'Batch_Year': 2020,
#     'Department_Name': 'Computer Science and Engineering',
#     'Total_Semesters': 8,
#     'Date': "14-11-2024",
#     'semesters': [
#         {
#             'Semester_Start': 'August',
#             'Acad_Start': 2020,
#             'Semester_End': 'December',
#             'Acad_End': 2020,
#             'courses': [
#                 {'Course_Name': 'Computer Programming', 'Course_Code': 'CS666', 'Course_Credit': 6,
#                  'Course_Grade': 'AA'},
#                 {'Course_Name': 'English', 'Course_Code': 'HS101', 'Course_Credit': 4, 'Course_Grade': 'AB'},
#                 {'Course_Name': 'Mathematics I', 'Course_Code': 'MA101', 'Course_Credit': 8, 'Course_Grade': 'BC'},
#                 {'Course_Name': 'Electrical Circuit Analysis', 'Course_Code': 'EC102', 'Course_Credit': 8,
#                  'Course_Grade': 'BB'},
#                 {'Course_Name': 'Digital Design Lab', 'Course_Code': 'EC110', 'Course_Credit': 3, 'Course_Grade': 'AA'},
#                 {'Course_Name': 'Digital Design', 'Course_Code': 'EC666', 'Course_Credit': 8, 'Course_Grade': 'AA'},
#                 {'Course_Name': 'Computer Programming Lab', 'Course_Code': 'CS110', 'Course_Credit': 5,
#                  'Course_Grade': 'BB'},
#                 {'Course_Name': 'Computer Programming', 'Course_Code': 'CS666', 'Course_Credit': 6,
#                  'Course_Grade': 'BC'}
#             ]
#         },
#         {
#             'Semester_Start': 'January',
#             'Acad_Start': 2021,
#             'Semester_End': 'May',
#             'Acad_End': 2021,
#             'courses': [
#                 {'Course_Name': 'Introduction to Politics', 'Course_Code': 'HS204', 'Course_Credit': 6,
#                  'Course_Grade': 'AA'},
#                 {'Course_Name': 'Basic Electronic Lab', 'Course_Code': 'EC111', 'Course_Credit': 3,
#                  'Course_Grade': 'AA'},
#                 {'Course_Name': 'Basic Electronic Circuits', 'Course_Code': 'EC103', 'Course_Credit': 8,
#                  'Course_Grade': 'AA'},
#                 {'Course_Name': 'Computer Organization', 'Course_Code': 'CS104', 'Course_Credit': 8,
#                  'Course_Grade': 'AB'},
#                 {'Course_Name': 'Data Structures Lab', 'Course_Code': 'CS111', 'Course_Credit': 3,
#                  'Course_Grade': 'BB'},
#                 {'Course_Name': 'Data Structures', 'Course_Code': 'CS103', 'Course_Credit': 8, 'Course_Grade': 'BC'},
#                 {'Course_Name': 'Mathematics II', 'Course_Code': 'MA102', 'Course_Credit': 8, 'Course_Grade': 'AB'}
#             ]
#         },
# {
#             'Semester_Start': 'August',
#             'Acad_Start': 2021,
#             'Semester_End': 'December',
#             'Acad_End': 2021,
#             'courses': [
#                 {'Course_Name': 'Mathematics III', 'Course_Code': 'MA203', 'Course_Credit': 6,
#                  'Course_Grade': 'AA'},
#                 {'Course_Name': 'Discrete Mathematics', 'Course_Code': 'MA205', 'Course_Credit': 6, 'Course_Grade': 'AB'},
#                 {'Course_Name': 'IT Workshop I', 'Course_Code': 'CS202', 'Course_Credit': 7, 'Course_Grade': 'AA'},
#                 {'Course_Name': 'Algorithms', 'Course_Code': 'CS201', 'Course_Credit': 6,
#                  'Course_Grade': 'AB'},
#                 {'Course_Name': 'Algorithm Lab', 'Course_Code': 'CS210', 'Course_Credit': 3, 'Course_Grade': 'AA'},
#                 {'Course_Name': 'Physics I', 'Course_Code': 'SC201', 'Course_Credit': 6, 'Course_Grade': 'AB'},
#                 {'Course_Name': 'Consumer Behaviour and Welfare Economics', 'Course_Code': 'HS205', 'Course_Credit': 6,
#                  'Course_Grade': 'BC'},
#             ]
#         },
#         {
#             'Semester_Start': 'January',
#             'Acad_Start': 2022,
#             'Semester_End': 'May',
#             'Acad_End': 2022,
#             'courses': [
#                 {'Course_Name': 'Operating Systems', 'Course_Code': 'CS231', 'Course_Credit': 6,
#                  'Course_Grade': 'AB'},
#                 {'Course_Name': 'Operating Systems Lab', 'Course_Code': 'CS232', 'Course_Credit': 3,
#                  'Course_Grade': 'AA'},
#                 {'Course_Name': 'Artificial Intelligence', 'Course_Code': 'CS235', 'Course_Credit': 6,
#                  'Course_Grade': 'BB'},
#                 {'Course_Name': 'Artificial Intelligence Lab', 'Course_Code': 'CS236', 'Course_Credit': 3,
#                  'Course_Grade': 'AA'},
#                 {'Course_Name': 'Database Management Systems', 'Course_Code': 'CS240', 'Course_Credit': 6,
#                  'Course_Grade': 'AA'},
#                 {'Course_Name': 'DBMS Lab', 'Course_Code': 'CS241', 'Course_Credit': 3, 'Course_Grade': 'AA'},
#                 {'Course_Name': 'Chemistry', 'Course_Code': 'SC202', 'Course_Credit': 6, 'Course_Grade': 'AA'},
#                 {'Course_Name': 'M.K. Gandhi - Modernity and Tradition', 'Course_Code': 'HS206', 'Course_Credit': 6, 'Course_Grade': 'AB'}
#
#             ]
#         },
# {
#             'Semester_Start': 'August',
#             'Acad_Start': 2022,
#             'Semester_End': 'December',
#             'Acad_End': 2022,
#             'courses': [
#                 {'Course_Name': 'Theory of Computation', 'Course_Code': 'CS301', 'Course_Credit': 8,
#                  'Course_Grade': 'BC'},
#                 {'Course_Name': 'Computer Networks', 'Course_Code': 'CS352', 'Course_Credit': 6, 'Course_Grade': 'AA'},
#                 {'Course_Name': 'Computer Networks Lab', 'Course_Code': 'CS353', 'Course_Credit': 3, 'Course_Grade': 'AA'},
#                 {'Course_Name': 'Machine Learning', 'Course_Code': 'CS306', 'Course_Credit': 6,
#                  'Course_Grade': 'AB'},
#                 {'Course_Name': 'Machine Learning Lab', 'Course_Code': 'CS360', 'Course_Credit': 3, 'Course_Grade': 'AA'},
#                 {'Course_Name': 'IT Workshop II', 'Course_Code': 'CS351', 'Course_Credit': 7, 'Course_Grade': 'AA'},
#                 {'Course_Name': 'Biology', 'Course_Code': 'SC301', 'Course_Credit': 6,
#                  'Course_Grade': 'AB'},
#                 {'Course_Name': 'Introduction to Folklore', 'Course_Code': 'HS407', 'Course_Credit': 6,
#                  'Course_Grade': 'AA'}
#             ]
#         },
#         {
#             'Semester_Start': 'January',
#             'Acad_Start': 2023,
#             'Semester_End': 'May',
#             'Acad_End': 2023,
#             'courses': [
#                 {'Course_Name': 'Optimization Techniques', 'Course_Code': 'MA305', 'Course_Credit': 6,
#                  'Course_Grade': 'BB'},
#                 {'Course_Name': 'Software Engineering', 'Course_Code': 'CS330', 'Course_Credit': 6,
#                  'Course_Grade': 'AB'},
#                 {'Course_Name': 'Software Engineering Lab', 'Course_Code': 'CS331', 'Course_Credit': 3,
#                  'Course_Grade': 'AB'},
#                 {'Course_Name': 'Compilers', 'Course_Code': 'CS320', 'Course_Credit': 6,
#                  'Course_Grade': 'AB'},
#                 {'Course_Name': 'Compilers Lab', 'Course_Code': 'CS321', 'Course_Credit': 3,
#                  'Course_Grade': 'AA'},
#                 {'Course_Name': 'Computer Security', 'Course_Code': 'CS361', 'Course_Credit': 6, 'Course_Grade': 'AB'},
#                 {'Course_Name': 'Storage Systems', 'Course_Code': 'CS332', 'Course_Credit': 6, 'Course_Grade': 'AA'},
#                 {'Course_Name': 'Physics II', 'Course_Code': 'SC302', 'Course_Credit': 6, 'Course_Grade': 'AA'},
#                 {'Course_Name': 'Advanced Communication Skills', 'Course_Code': 'HS307', 'Course_Credit': 6, 'Course_Grade': 'AB'}
#
#             ]
#         },
# {
#             'Semester_Start': 'August',
#             'Acad_Start': 2023,
#             'Semester_End': 'December',
#             'Acad_End': 2023,
#             'courses': [
#                 {'Course_Name': 'Projects', 'Course_Code': 'CS501', 'Course_Credit': 12,
#                  'Course_Grade': 'AA'},
#                 {'Course_Name': 'Data Analytics', 'Course_Code': 'CS502', 'Course_Credit': 6, 'Course_Grade': 'AB'},
#                 {'Course_Name': 'Natural Language Processing', 'Course_Code': 'CS503', 'Course_Credit': 6, 'Course_Grade': 'BB'},
#                 {'Course_Name': 'NPTEL- Design and Implementation', 'Course_Code': 'CS504', 'Course_Credit': 6,
#                  'Course_Grade': 'BB'},
#                 {'Course_Name': 'Democracy Politics', 'Course_Code': 'HS509', 'Course_Credit': 6, 'Course_Grade': 'BB'},
#             ]
#         },
#         {
#             'Semester_Start': 'January',
#             'Acad_Start': 2020,
#             'Semester_End': 'May',
#             'Acad_End': 2021,
#             'courses': [
#                 {'Course_Name': 'Financial Management', 'Course_Code': 'CS204', 'Course_Credit': 6,
#                  'Course_Grade': 'BB'},
#                 {'Course_Name': 'Intellectual Property Right for Information Technology', 'Course_Code': 'EC111', 'Course_Credit': 3,
#                  'Course_Grade': 'AB'},
#                 {'Course_Name': 'Internship', 'Course_Code': 'CS444', 'Course_Credit': 18,
#                  'Course_Grade': 'AA'},
#             ]
#         },
#     ],
#     'SPI_Name': 'S.P.I',
#     'CPI_Name': 'C.P.I',
#     'SPI_CPI': {'Sem_1_spi': Decimal('8.25'), 'Sem_1_cpi': Decimal('8.25'), 'Sem_2_spi': Decimal('8.95'),
#                 'Sem_2_cpi': Decimal('8.63'),'Sem_3_spi': Decimal('8.25'), 'Sem_3_cpi': Decimal('8.25'), 'Sem_4_spi': Decimal('8.95'),
#                 'Sem_4_cpi': Decimal('8.63'),'Sem_5_spi': Decimal('8.25'), 'Sem_5_cpi': Decimal('8.25'), 'Sem_6_spi': Decimal('8.95'),
#                 'Sem_6_cpi': Decimal('8.63'),'Sem_7_spi': Decimal('8.83'), 'Sem_7_cpi': Decimal('8.99'), 'Sem_8_spi': Decimal('9.40'),
#                 'Sem_8_cpi': Decimal('9.04')},
#     'is_completed': 'COMPLETE'
# }

def draw_header(c, institute_name, logo_path):
    c.setFont("Helvetica-Bold", 14)
    # Draw the institute name at the top center
    c.drawCentredString(A4[0]/2, A4[1] - 40, institute_name)
    # Draw the institute logo at the top left
    c.drawImage(logo_path, 20, A4[1] - 70, width=50, height=50, preserveAspectRatio=True)
    c.line(0, A4[1] - 70, A4[0], A4[1] - 70)



def wrap_text(text, max_width, canvas, font_name="Helvetica", font_size=10):
    """
    Wrap text to fit within a specified width.
    """
    canvas.setFont(font_name, font_size)
    words = text.split()
    lines = []
    line = ""
    for word in words:
        # Check width of the line if we add the next word
        test_line = f"{line} {word}".strip()
        if canvas.stringWidth(test_line, font_name, font_size) <= max_width:
            line = test_line
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines

def generate_pdf(data, institute_name, logo_path):
    pdf_io = BytesIO()
    c = canvas.Canvas(pdf_io, pagesize=A4)
    width, height = A4

    # Add Title
    c.setFont("Helvetica-Bold", 16)
    draw_header(c, institute_name, logo_path)
    c.drawString(220, height - 100, f"Student Report Card")

    # Personal Information
    c.setFont("Helvetica", 12)
    c.drawString(60, height - 130, f"Roll Number: {data['Roll_Number']}")
    c.drawString(260, height - 130, f"Program: {data['Program_Name']}")
    c.drawString(60, height - 150, f"Batch Year: {data['Batch_Year']}")
    c.drawString(260, height - 150, f"Department: {data['Department_Name']}")
    c.line(0, height - 170, A4[0], height - 170)
    # Semester Blocks
    block_height = (height - 250) / 2
    block_width = width / 2
    margin_x = 30
    margin_y = 240
    block_index = 0
    semesters_iterated = 0

    for semester in data['semesters']:
        # Position for each block
        x = margin_x + (block_index % 2) * block_width
        y = height - margin_y - (block_index // 2) * block_height

        # Semester Header
        c.setFont("Helvetica-Bold", 10)
        semester_title = f"Semester {semesters_iterated + 1}: {semester['Semester_Start']} {semester['Acad_Start']} - {semester['Semester_End']} {semester['Acad_End']}"
        c.drawString(x, y, semester_title)
        y -= 20

        # Table Header for Courses
        headers = ["Course Name", "Course Code", "Credits", "Grade"]
        header_x = x
        header_widths = [125, 60, 50, 40]
        c.setFont("Helvetica-Bold", 9)

        # Draw headers
        for i, header in enumerate(headers):
            c.drawString(x + sum(header_widths[:i]), y, header)

        y -= 15

        # Draw Course Rows
        c.setFont("Helvetica", 8)
        for course in semester['courses']:
            course_name_wrapped = wrap_text(course['Course_Name'], header_widths[0], c)
            course_code = course['Course_Code']
            course_credit = str(course['Course_Credit'])
            course_grade = course['Course_Grade']
            y_position = y
            for line in course_name_wrapped:
                c.drawString(x, y_position, line)
                y_position -= 12  # Adjust line spacing

            # Other columns
            c.drawString(x + header_widths[0], y, course_code)
            c.drawString(x + header_widths[0] + header_widths[1], y, course_credit)
            c.drawString(x + header_widths[0] + header_widths[1] + header_widths[2], y, course_grade)
            y -= max(15, 12 * len(course_name_wrapped))

        block_index += 1
        semesters_iterated+=1

        if block_index%4==0 and semesters_iterated<len(data['semesters']):
            c.showPage()
            draw_header(c, institute_name, logo_path)
            block_index=0


    # Add SPI/CPI Table on a new page
    c.showPage()
    draw_header(c, institute_name, logo_path)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(A4[0] / 2, height - 150, f"{data['SPI_Name']} and {data['CPI_Name']} Table")

    # Draw table with border
    x_pos, y_pos = 210, height - 240
    headers = ["Semester", data['SPI_Name'], data['CPI_Name']]
    c.rect(x_pos - 60, y_pos + 20, 300, -25 * (data['Total_Semesters'] + 2))
    for header in headers:
        c.drawCentredString(x_pos, y_pos, header)
        x_pos += 100
    c.line(150, y_pos-8, 450, y_pos-8)
    y_pos -= 30
    c.setFont("Helvetica", 16)

    # Table Rows
    for i in range(1, data['Total_Semesters'] + 1):
        x_pos = 210
        spi_key = f"Sem_{i}_spi"
        cpi_key = f"Sem_{i}_cpi"
        c.drawCentredString(x_pos, y_pos, f"Semester {i}")
        c.drawCentredString(x_pos + 100, y_pos, str(data['SPI_CPI'].get(spi_key, "-")))
        c.drawCentredString(x_pos + 200, y_pos, str(data['SPI_CPI'].get(cpi_key, "-")))
        y_pos -= 25
    c.drawString(x_pos, y_pos - 50, f"Status: {data['is_completed']}")
    c.drawString(50, 55, f"Date: {data['Date']}")


    # Add a description and grading rules on the last page
    c.showPage()
    draw_header(c, institute_name, logo_path)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(220, height - 100, "Grades and Calculation Rules")
    c.setFont("Helvetica", 8)
    rules_text = """
     Letter Grade : Grade Points 
     AA           : 10           
     AB           : 9            
     BB           : 8            
     BC           : 7            
     CC           : 6            
     CD           : 5            
     DD           : 4            
     F            : 0 (Fail)     
     PP           : Pass         

    Abbreviations Used:
    - Cr. : Credit
    - Gr. : Grade
    - S.P.I. : Semester Performance Index
    - C.P.I. : Cumulative Performance Index

    - A student is considered to have successfully completed a subject and earned credits if they secure a letter grade other than "I" or "F" in that subject.
    - A grade of "F" indicates failure in a course. In the case of a theory course, the student may pass the course by taking a supplementary examination. 
      The highest grade attainable through this option is CC.
    - If a student fails to clear the course in two supplementary attempts, they must repeat the course.
    - For a Laboratory/Practical subject failure, the student must re-register for the course in the next appropriate semester 
      and can earn up to a letter grade of AA.
    - When a student repeats a course or takes a supplementary examination, two grades will be recorded for that course. 
      Supplementary examination grades will be shown separately, and the higher of the two grades will be used in S.P.I. and C.P.I. calculations.

    No Class or Division is awarded at this Institute.

    S.P.I. and C.P.I. Calculations:
    - S.P.I. (Semester Performance Index):
      S.P.I. = ∑(Ci * Gi) / ∑(Ci)

    - C.P.I. (Cumulative Performance Index):
      C.P.I. = ∑(Ci * Gi) / ∑(Ci)

    Where:
    - Ci = Credits assigned to a course
    - Gi = Grade points corresponding to the grade awarded for the course
    - N = Total number of courses registered in a semester
    - M = Total number of courses registered to date

    Note: IIIT Guwahati does not provide a formula for converting CPI to percentage marks. 
    If required, an indicative percentage can be obtained by multiplying the CPI by 10.
    """
    y_pos = height - 110
    for line in rules_text.splitlines():
        c.drawString(40, y_pos, line)
        y_pos -= 15
    c.setFont("Helvetica-Bold", 10)

    # Save PDF
    c.save()
    pdf_io.seek(0)
    return pdf_io

def get_student_pdf(data):
    print(data)
    return generate_pdf(data, "Indian Institute of Information Technology Guwahati", "/Users/heenamatlani/PycharmProjects/GradeChakra/backend/services/img.png")
