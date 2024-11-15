INSERT INTO Programs (program_short_name, program_full_name, total_semesters) VALUES
('BTech', 'Bachelor of Technology', 8),
('MTech', 'Master of Technology', 4),
('PhD', 'Doctor of Philosophy', 6);

INSERT INTO Departments (department_short_name, department_full_name) VALUES
('CSE', 'Computer Science and Engineering'),
('ECE', 'Electronics and Communication Engineering'),
('ME', 'Mechanical Engineering');

INSERT INTO Batches (batch_year, program_id) VALUES
(2020, 1),  -- BTech
(2021, 1),
(2019, 2),  -- MTech
(2022, 3);  -- PhD

INSERT INTO Roles (role_name) VALUES
('HOD'),
('Dean'),
('Professor'),
('Assistant Professor'),
('Lecturer'),
('Registrar');

INSERT INTO User_Types (type_name) VALUES
('Admin'),s
('Faculty'),
('Academic Staff');

INSERT INTO Employees (first_name, last_name, email, password, department_id, role_id, user_type_id, start_date, end_date) VALUES
('Gautam', 'Barua', 'gautam.barua@iiitg.ac.in', 'hashed_password', 1, 1, 2, '2010-06-01', NULL),  -- HOD of CSE, Faculty
('Anjali', 'Mehra', 'anjali.mehra@iiitg.ac.in', 'hashed_password', 2, 1, 2, '2015-08-01', NULL),  -- HOD of ECE, Faculty
('Raj', 'Sharma', 'raj.sharma@iiitg.ac.in', 'hashed_password', 1, 2, 1, '2020-01-01', NULL),  -- Dean of CSE, Admin
('Pooja', 'Nair', 'pooja.nair@iiitg.ac.in', 'hashed_password', 3, 3, 3, '2019-09-01', '2023-09-01');  -- Lecturer in ME, Academic Staff

UPDATE Employees
SET college_employee_id = CASE employee_id
    WHEN 1 THEN 'CSE-001'
    WHEN 2 THEN 'ECE-001'
    WHEN 3 THEN 'CSE-002'
    WHEN 4 THEN 'ME-001'
    ELSE 'UNKNOWN'
END;

INSERT INTO Employees (college_employee_id, first_name, last_name, email, password, department_id, role_id, user_type_id, start_date, end_date) VALUES
('CSE-101', 'Amit', 'Kumar', 'amit.kumar@iiitg.ac.in', 'hashed_password', 1, 1, 2, '2015-06-01', NULL),    -- Professor
('CSE-102', 'Radhika', 'Sharma', 'radhika.sharma@iiitg.ac.in', 'hashed_password', 1, 2, 2, '2016-09-15', NULL),  -- Associate Professor
('CSE-103', 'Vivek', 'Singh', 'vivek.singh@iiitg.ac.in', 'hashed_password', 1, 3, 2, '2017-08-20', NULL),   -- Assistant Professor
('CSE-104', 'Meera', 'Rao', 'meera.rao@iiitg.ac.in', 'hashed_password', 1, 3, 2, '2018-05-10', NULL),      -- Assistant Professor
('CSE-105', 'Nikhil', 'Patel', 'nikhil.patel@iiitg.ac.in', 'hashed_password', 1, 4, 2, '2019-01-05', NULL), -- Lecturer
('CSE-106', 'Sneha', 'Kapoor', 'sneha.kapoor@iiitg.ac.in', 'hashed_password', 1, 4, 2, '2020-02-11', NULL), -- Lecturer
('CSE-107', 'Ankit', 'Verma', 'ankit.verma@iiitg.ac.in', 'hashed_password', 1, 5, 2, '2021-03-01', NULL),   -- Research Associate
('CSE-108', 'Deepika', 'Gupta', 'deepika.gupta@iiitg.ac.in', 'hashed_password', 1, 3, 2, '2022-06-15', NULL), -- Assistant Professor
('CSE-109', 'Rahul', 'Mehta', 'rahul.mehta@iiitg.ac.in', 'hashed_password', 1, 2, 2, '2019-11-20', NULL),   -- Associate Professor
('CSE-110', 'Priya', 'Joshi', 'priya.joshi@iiitg.ac.in', 'hashed_password', 1, 1, 2, '2014-07-01', NULL);   -- Professor

INSERT INTO Students (roll_number, first_name, last_name, email, batch_id, department_id, password) VALUES
('B202001001', 'Heena', 'Matlani', 'heena.matlani@iiitg.ac.in', 1, 1, 'hashed_password'),  -- BTech, CSE
('B202101002', 'Rahul', 'Kumar', 'rahul.kumar@iiitg.ac.in', 2, 1, 'hashed_password'),      -- BTech, CSE
('B202101003', 'Megha', 'Singh', 'megha.singh@iiitg.ac.in', 2, 2, 'hashed_password'),      -- BTech, ECE
('M201901001', 'Amit', 'Patel', 'amit.patel@iiitg.ac.in', 3, 1, 'hashed_password'),        -- MTech, CSE
('P202201001', 'Suman', 'Roy', 'suman.roy@iiitg.ac.in', 4, 2, 'hashed_password');          -- PhD, ECE

INSERT INTO Batch_Role_Assignment (batch_id, role_id) VALUES
(1, 3),  -- Assign Professor role to Batch 2020
(2, 3),  -- Assign Professor role to Batch 2021
(3, 6);  -- Assign Registrar role to MTech Batch 2019

INSERT INTO Academic_Year (start_year, end_year) VALUES
(2020, 2021),
(2021, 2022),
(2022, 2023);

INSERT INTO Semester_Name (semester_name) VALUES
('Monsoon'),
('Winter'),
('Summer');

INSERT INTO Semesters (semester_name_id, academic_year_id, start_month, end_month) VALUES
(1, 1, 'August', 'December'),  -- Monsoon Semester, 2020-2021
(2, 1, 'January', 'May'),      -- Winter Semester, 2020-2021
(1, 2, 'August', 'December'),  -- Monsoon Semester, 2021-2022
(2, 2, 'January', 'May'),      -- Winter Semester, 2021-2022
(3, 3, 'May', 'July');         -- Summer Semester, 2022-2023


INSERT INTO Courses (course_code, course_name, credits, department_id, is_lab_course) VALUES
('CS666', 'Computer Programming', 6, 1, FALSE),
('CS110', 'Computer Programming Lab', 5, 1, TRUE),
('EC666', 'Digital Design', 8, 2, FALSE),
('EC110', 'Digital Design Lab', 3, 2, TRUE),
('EC102', 'Electrical Circuit Analysis', 8, 2, FALSE),
('MA101', 'Mathematics I', 8, 1, FALSE),
('HS101', 'English', 4, 1, FALSE),
('MA102', 'Mathematics II', 8, 1, FALSE),
('CS103', 'Data Structures', 8, 1, FALSE),
('CS111', 'Data Structures Lab', 3, 1, TRUE),
('CS104', 'Computer Organization', 8, 1, FALSE),
('EC103', 'Basic Electronic Circuits', 8, 2, FALSE),
('EC111', 'Basic Electronic Lab', 3, 2, TRUE),
('HS204', 'Introduction to Politics', 6, 1, FALSE);


INSERT INTO Notifications (student_id, message, date_sent, is_read) VALUES
(1, 'Your grades for the Winter Semester 2023 have been uploaded.', '2023-10-05', FALSE),
(2, 'Please check your Monsoon Semester 2022 grades. Feedback on discrepancies is open until October 15th.', '2023-09-25', TRUE),
(3, 'Supplementary exam for Fluid Mechanics is scheduled for November 5th.', '2023-09-28', FALSE),
(4, 'Your grade in Communication Systems has been updated after re-evaluation.', '2023-08-01', TRUE),
(1, 'Database Management Systems grade re-evaluation is complete. Check the results in your account.', '2023-08-10', TRUE);

-- Insert 20 student issues
INSERT INTO IssuesRequests (sender_type, student_id, issue_text, date_submitted, is_read)
VALUES
('student', 1, 'Incorrect grade recorded for CS101. Expected AA but recorded as AB.', '2024-10-01', FALSE),
('student', 2, 'My CPI is showing as 7.2, but it should be 8.0. Please verify.', '2024-10-02', FALSE),
('student', 3, 'Grade for MA102 seems incorrect. Expected BB but received BC.', '2024-10-03', FALSE),
('student', 4, 'My result for PH105 is marked as incomplete, please check.', '2024-10-04', TRUE),
('student', 5, 'Got F in CS201 but submitted all assignments. Request review.', '2024-10-05', FALSE),
('student', 1, 'CPI discrepancy in my record. Showing 6.9 instead of 7.3.', '2024-10-06', TRUE),
('student', 2, 'Grades for EE204 showing incorrect SPI for semester 4.', '2024-10-07', FALSE),
('student', 3, 'Issue in grade calculation for elective CS303.', '2024-10-08', TRUE),
('student', 4, 'Grade recorded as F in elective, but I passed the exam.', '2024-10-09', FALSE),
('student', 1, 'Expected AB in CS105, received CC instead. Please verify.', '2024-10-10', FALSE),
('student', 1, 'PH102 lab grade marked lower than expected.', '2024-10-11', TRUE),
('student', 2, 'Issue with recorded grades for Humanities elective.', '2024-10-12', FALSE),
('student', 3, 'Wrong SPI shown for semester 6 in my profile.', '2024-10-13', FALSE),
('student', 4, 'Grades for MA203 need re-evaluation, recorded lower than expected.', '2024-10-14', TRUE),
('student', 5, 'My CPI is incorrect due to wrong MA104 grades.', '2024-10-15', FALSE),
('student', 1, 'Failed in core course wrongly. I submitted all coursework.', '2024-10-16', FALSE),
('student', 1, 'Incorrect grading for CS305, expected B but received D.', '2024-10-17', TRUE),
('student', 1, 'Issue in SPI calculation for recent semester.', '2024-10-18', FALSE),
('student', 1, 'Recorded grade for elective History is incorrect.', '2024-10-19', FALSE),
('student', 2, 'Wrong grade entry for Digital Logic Design course.', '2024-10-20', FALSE);

-- Insert 20 faculty requests
INSERT INTO IssuesRequests (sender_type, faculty_id, issue_text, date_submitted, is_read)
VALUES
('faculty', 1, 'Request to change student 2\'s grade in CS101 from B to A.', '2024-10-01', TRUE),
('faculty', 2, 'Student 3 requested grade change in MA102 from C to B.', '2024-10-02', FALSE),
('faculty', 1, 'Update grade for student 5 in PH105 to reflect recent evaluation.', '2024-10-03', TRUE),
('faculty', 1, 'Change student 7\'s grade in CS201 from D to C.', '2024-10-04', FALSE),
('faculty', 1, 'Request grade adjustment for student 9 in CS202.', '2024-10-05', TRUE),
('faculty', 2, 'Grade change for student 10 in EE204 from F to D due to error.', '2024-10-06', FALSE),
('faculty', 2, 'Request to update student 11\'s CS301 grade after retake.', '2024-10-07', FALSE),
('faculty', 2, 'Adjust grade for student 12 in CS303 elective.', '2024-10-08', TRUE),
('faculty', 2, 'Student 13 requested a re-evaluation of CS104 grade.', '2024-10-09', FALSE),
('faculty', 1, 'Update student 14\'s grade in PH103 as per department recommendation.', '2024-10-10', TRUE),
('faculty', 1, 'Change grade for student 15 in CS201 to reflect exam score.', '2024-10-11', FALSE),
('faculty', 2, 'Request adjustment for student 16 in CS106.', '2024-10-12', TRUE),
('faculty', 1, 'Adjust student 17\'s grade in EE203 from D to C after review.', '2024-10-13', FALSE),
('faculty', 1, 'Change student 18\'s MA201 grade due to miscalculation.', '2024-10-14', TRUE),
('faculty', 1, 'Student 19 has applied for re-evaluation in CS305.', '2024-10-15', FALSE),
('faculty', 1, 'Update student 20\'s PH202 grade to reflect practical exam score.', '2024-10-16', TRUE),
('faculty', 1, 'Adjust CS101 grade for student 1 after final review.', '2024-10-17', FALSE),
('faculty', 1, 'Request to change CS203 grade for student 2.', '2024-10-18', TRUE),
('faculty', 1, 'Adjust MA104 grade for student 4 due to attendance waiver.', '2024-10-19', FALSE),
('faculty', 2, 'Re-evaluate CS102 grade for student 8.', '2024-10-20', TRUE);


INSERT INTO Course_Repeat_Policy (replacement_id) VALUES
(1), -- replace_with_higher_grade
(2), -- average_of_grades
(3), -- most_recent_grade
(4); -- replace_f_grade

INSERT INTO Lab_Course_Repeat_Policy (replacement_id) VALUES
(1), -- replace_with_higher_grade
(2), -- average_of_grades
(3), -- most_recent_grade
(4); -- replace_f_grade

INSERT INTO Year_Repetition_Display (display_option_id) VALUES
(1),
(2),
(3);

INSERT INTO Course_Repeat_And_Supplementary_Display (display_option_id) VALUES
(1),
(2),
(3);

-- Assigning API Access to Roles
INSERT INTO API_Role_Access (role_id, api_id) VALUES
-- Grading Rules and Calculation API for Admins
(1, 1),

-- Grade Upload API for Academic Staff and Admins
(1, 2),
(2, 2);

INSERT INTO Logs (employee_id, action_id, description, timestamp) VALUES
(1, 1, 'Grading system set for batch 2022 BTech CSE.', '2024-10-01 09:30:00'),
(2, 2, 'Uploaded grades for 2024 semester 1 for batch 2023 BTech ECE.', '2024-10-02 14:15:00'),
(3, 3, 'Updated PDF description for grade reports to include footer for batch 2022.', '2024-10-02 10:20:00'),
(1, 1, 'Grading system changed for batch 2023 BTech CSE.', '2024-10-03 11:00:00'),
(4, 4, 'Updated grading system for batch 2021 MTech CSE.', '2024-10-03 12:45:00'),
(2, 5, 'Changed role of faculty member (ID: 5) from Lecturer to Assistant Professor.', '2024-10-03 13:30:00'),
(4, 2, 'Uploaded supplementary exam grades for batch 2021 BTech CSE.', '2024-10-04 15:10:00'),
(1, 1, 'Grading system updated for batch 2022 BTech ECE.', '2024-10-05 09:45:00'),
(2, 3, 'Set new PDF description for grade reports for batch 2023 BTech ECE.', '2024-10-05 11:20:00'),
(3, 2, 'Uploaded final grades for 2024 semester 2 for batch 2023 MTech CSE.', '2024-10-06 16:40:00'),
(1, 1, 'Grading system updated for batch 2022 BTech CSE to reflect new grade replacement rules.', '2024-10-06 17:00:00'),
(4, 5, 'Changed role of employee (ID: 7) from Lab Assistant to Senior Lab Assistant.', '2024-10-07 10:10:00'),
(2, 2, 'Uploaded grades for 2024 semester 2 for batch 2023 BTech ECE.', '2024-10-07 14:05:00'),
(2, 1, 'Grading system set for batch 2024 BTech IT.', '2024-10-08 10:00:00'),
(3, 4, 'Updated grading system for batch 2022 MTech CSE to reflect new CPI calculation.', '2024-10-08 11:30:00');

