CREATE DATABASE GradeManagementSystem;

USE GradeManagementSystem;

CREATE TABLE Students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    roll_number VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE NOT NULL,
    batch_id INT,
    department_id INT,
    password VARBINARY(255) NOT NULL,
    FOREIGN KEY (batch_id) REFERENCES Batches(batch_id)
	ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (department_id) REFERENCES Departments(department_id)
	ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Programs (
    program_id INT AUTO_INCREMENT PRIMARY KEY,
    program_short_name VARCHAR(20) UNIQUE,
    program_full_name VARCHAR(100) UNIQUE,
    total_semesters INT
);

CREATE TABLE Departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    department_short_name VARCHAR(20) UNIQUE,
    department_full_name VARCHAR(100) UNIQUE
);

CREATE TABLE Batches (
    batch_id INT AUTO_INCREMENT PRIMARY KEY,
    batch_year INT,
    program_id INT,
    FOREIGN KEY (program_id) REFERENCES Programs(program_id)
	ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Employees (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    college_employee_id INT UNIQUE,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARBINARY(255) NOT NULL,
    department_id INT,
    role_id INT,
    user_type_id INT,
    start_date DATE,
    end_date DATE,
    FOREIGN KEY (department_id) REFERENCES Departments(department_id)
	ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (role_id) REFERENCES Roles(role_id)
	ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (user_type_id) REFERENCES User_Types(user_type_id)
	ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Roles (
    role_id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE User_Types (
    user_type_id INT AUTO_INCREMENT PRIMARY KEY,
    type_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE Batch_Role_Assignment (
    assignment_id INT AUTO_INCREMENT PRIMARY KEY,
    batch_id INT,
    role_id INT,
    FOREIGN KEY (batch_id) REFERENCES Batches(batch_id)
	ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (role_id) REFERENCES Roles(role_id)
	ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_code VARCHAR(20) UNIQUE NOT NULL,
    course_name VARCHAR(100) UNIQUE NOT NULL,
    credits INT,
    department_id INT,
    is_lab_course BOOLEAN,
    FOREIGN KEY (department_id) REFERENCES Departments(department_id)
	ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Academic_Year (
    academic_year_id INT AUTO_INCREMENT PRIMARY KEY,
    start_year INT,
    end_year INT
);


CREATE TABLE Semester_Name (
    semester_name_id INT AUTO_INCREMENT PRIMARY KEY,
    semester_name VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE Semesters (
    semester_id INT AUTO_INCREMENT PRIMARY KEY,
    semester_name_id INT,
    academic_year_id INT,
    start_month VARCHAR(20),
    end_month VARCHAR(20),
    FOREIGN KEY (semester_name_id) REFERENCES Semester_Name(semester_name_id)
	ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (academic_year_id) REFERENCES Academic_Year(academic_year_id)
	ON DELETE CASCADE ON UPDATE CASCADE

);

CREATE TABLE Grades (
    grade_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    course_id INT,
    semester_id INT,
    employee_id INT,
    numeric_grade DECIMAL(5,2) NULL,
    special_grade_id INT NULL,
    grade_type_id INT,
    elective_change BOOLEAN,
    new_course_id INT,
    previous_course_id INT,
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
	ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
	ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (semester_id) REFERENCES Semesters(semester_id)
	ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
	ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (special_grade_id) REFERENCES Special_Grades(special_grades_id)
	ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (grade_type_id) REFERENCES Grade_Types(grade_type_id)
	ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Grade_Types (
	grade_type_id INT AUTO_INCREMENT PRIMARY KEY,
	type_name VARCHAR(20) UNIQUE NOT NULL
);


CREATE TABLE Grade_Replacement_Rules (
    replacement_id INT AUTO_INCREMENT PRIMARY KEY,
    rule_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT
);


CREATE TABLE SPI_Formula (
    spi_formula_id INT AUTO_INCREMENT PRIMARY KEY,
    formula_name VARCHAR(255) UNIQUE NOT NULL,
    formula TEXT NOT NULL
);

CREATE TABLE CPI_Formula (
    cpi_formula_id INT AUTO_INCREMENT PRIMARY KEY,
    formula_name VARCHAR(255) UNIQUE NOT NULL,
    formula TEXT NOT NULL
);

CREATE TABLE SPI_CPI_Rules (
    spi_cpi_rule_id INT AUTO_INCREMENT PRIMARY KEY,
    spi_formula_id INT,
    cpi_formula_id INT,
    spi_name VARCHAR(50) NOT NULL,
    cpi_name VARCHAR(50) NOT NULL,
    round_to_decimal_places INT NOT NULL,
    FOREIGN KEY (spi_formula_id) REFERENCES SPI_Formula(spi_formula_id)
	ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (cpi_formula_id) REFERENCES CPI_Formula(cpi_formula_id)
	ON DELETE CASCADE ON UPDATE CASCADE
);



CREATE TABLE SPI_CPI (
    spi_cpi_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    semester_id INT,
    spi DECIMAL(5,2) NOT NULL,
    cpi DECIMAL(5,2) NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
	ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (semester_id) REFERENCES Semesters(semester_id)
	ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Year_Repetition_Rules (
    year_repeat_rule_id INT AUTO_INCREMENT PRIMARY KEY,
    rule_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE Grading_Details (
    grading_details_id INT AUTO_INCREMENT PRIMARY KEY,
    system_type ENUM('numeric', 'special'),
    max_score INT NOT NULL,
    use_best_n_of_m BOOLEAN NOT NULL,
    best_n INT,
    total_m INT
);

CREATE TABLE Special_Grades (
    special_grades_id INT AUTO_INCREMENT PRIMARY KEY,
    grade VARCHAR(2) NOT NULL,
    grade_point DECIMAL(4,2) NOT NULL,
    grading_details_id INT,
    FOREIGN KEY (grading_details_id) REFERENCES Grading_Details(grading_details_id)
	ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Course_Repeat_Policy (
    course_repeat_policy_id INT AUTO_INCREMENT PRIMARY KEY,
    replacement_id INT,
    FOREIGN KEY (replacement_id) REFERENCES Grade_Replacement_Rules(replacement_id)
	ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Lab_Course_Repeat_Policy (
    lab_course_repeat_policy_id INT AUTO_INCREMENT PRIMARY KEY,
    replacement_id INT,
    FOREIGN KEY (replacement_id) REFERENCES Grade_Replacement_Rules(replacement_id)
	ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Display_Options (
    display_option_id INT AUTO_INCREMENT PRIMARY KEY,
    option_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE Year_Repetition_Display (
    year_repetition_display_id INT AUTO_INCREMENT PRIMARY KEY,
    display_option_id INT,
    FOREIGN KEY (display_option_id) REFERENCES Display_Options(display_option_id)
	ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Course_Repeat_And_Supplementary_Display (
    course_repeat_and_supplementary_display_id INT AUTO_INCREMENT PRIMARY KEY,
    display_option_id INT,
    FOREIGN KEY (display_option_id) REFERENCES Display_Options(display_option_id)
	ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Grading_System_Configuration (
    grading_system_config_id INT AUTO_INCREMENT PRIMARY KEY,
    grading_details_id INT,
    year_repetition_id INT,
    course_repeat_policy_id INT,
    lab_course_repeat_policy_id INT,
    year_repetition_display_id INT,
    course_repeat_and_supplementary_display_id INT,
    spi_cpi_rule_id INT,
    start_batch_year INT,
    end_batch_year INT,
    is_active BOOLEAN,
    FOREIGN KEY (grading_details_id) REFERENCES Grading_Details(grading_details_id)
	ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (year_repetition_id) REFERENCES Year_Repetition_Rules(year_repeat_rule_id)
	ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (course_repeat_policy_id) REFERENCES Course_Repeat_Policy(course_repeat_policy_id)
	ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (lab_course_repeat_policy_id) REFERENCES Lab_Course_Repeat_Policy(lab_course_repeat_policy_id)
	ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (year_repetition_display_id) REFERENCES Year_Repetition_Display(year_repetition_display_id)
	ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (course_repeat_and_supplementary_display_id) REFERENCES Course_Repeat_And_Supplementary_Display(course_repeat_and_supplementary_display_id)
	ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (spi_cpi_rule_id) REFERENCES SPI_CPI_Rules(spi_cpi_rule_id)
	ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE APIs (
    api_id INT AUTO_INCREMENT PRIMARY KEY,
    api_name VARCHAR(100) UNIQUE NOT NULL,
    url VARCHAR(255) UNIQUE NOT NULL,
    description VARCHAR(500),
    example_json VARCHAR(1000)
);

CREATE TABLE API_Role_Access (
    api_access_id INT AUTO_INCREMENT PRIMARY KEY,
    role_id INT,
    api_id INT,
    FOREIGN KEY (role_id) REFERENCES Roles(role_id)
	ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (api_id) REFERENCES APIs(api_id)
	ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    action_id INT,
    description TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
	ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (action_id) REFERENCES Actions(action_id)
	ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Actions (
    action_id INT AUTO_INCREMENT PRIMARY KEY,
    action_type VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IssuesRequests (
    request_id INT AUTO_INCREMENT PRIMARY KEY,
    sender_type ENUM('student', 'faculty') NOT NULL,  -- Indicates if the sender is a student or faculty
    student_id INT NULL, -- Student ID if the sender is a student
    faculty_id INT NULL, -- Faculty ID if the sender is a faculty member
    issue_text TEXT NOT NULL, -- Content of the issue or request
    date_submitted DATE DEFAULT (CURRENT_TIMESTAMP), -- Date the issue/request was submitted
    is_read BOOLEAN DEFAULT FALSE, -- Tracks if the issue/request has been marked as read
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (faculty_id) REFERENCES Employees(employee_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE Notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    message TEXT,
    date_sent DATE,
    is_read BOOLEAN,
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
	ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE PDF_Description (
    pdf_description_id INT AUTO_INCREMENT PRIMARY KEY,
    grading_system_config_id INT,
    description TEXT,
    is_active BOOLEAN,
    FOREIGN KEY (grading_system_config_id) REFERENCES Grading_System_Configuration(grading_system_config_id)
	ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE StudentGradeReports (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    semester_id INT NOT NULL,
    grade_pdf LONGBLOB NOT NULL,  -- Stores the binary data of the PDF file
    date_generated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Date the PDF was generated
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,  -- Date of the last update

    -- Foreign key constraints
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (semester_id) REFERENCES Semesters(semester_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);


INSERT INTO Year_Repetition_Rules (rule_name, description) VALUES
('reset_previous_results', 'Reset all grades for the year when a student repeats the year.'),
('keep_previous_results', 'Retain grades from previous years, even if the year is repeated and use them while calculating result.'),
('replace_failed_courses_only', 'Only replace grades for courses that were failed, keeping the rest.');

INSERT INTO Grade_Replacement_Rules (rule_name, description) VALUES
('replace_with_higher_grade', 'Replace the lower grade with the higher grade if a course is repeated.'),
('average_of_grades', 'Calculate the average of the grades if a course is repeated.'),
('most_recent_grade', 'Keep the most recent grade if a course is repeated.'),
('replace_f_grade', 'Replace an F grade with the new grade obtained after repeating the course.');

INSERT INTO Display_Options (option_name, description) VALUES
('show_previous_results_with_asterisk', 'Show previous results along with new grades, marking new grades with an asterisk.'),
('hide_previous_results', 'Do not show previous grades when a student repeats a course.'),
('just_mark_with_asterisk', 'Mark repeated years with an asterisk (*) without showing previous results.');

INSERT INTO APIs (api_name, url, description, example_json) VALUES
-- 1. Grading Rules and Calculation API
('Grading Rules and Calculation API', '/set-grading-rules',
'This API allows administrators to configure the grading system rules, including grade types, maximum scores, grade points mapping, semester weightage, and other institute-specific rules.',
'{
  "grading_system": {
    "type": "special",
    "grades": {
      "AA": 10,
      "AB": 9,
      "BB": 8,
      "BC": 7,
      "CC": 6,
      "CD": 5,
      "DD": 4,
      "F": 0
    },
    "max_score": 10.0,
    "use_best_n_of_m": "use_best_5_of_7"
  },
  "year_repetition": {
    "rule": "reset_previous_results",
    "display": "show_previous_results_with_asterisk"
  },
  "course_repeat": "replace_with_higher_grade",
  "lab_course_repeat": "average_of_grades",
  "course_repeat_and_supplementary_display": "show_previous_results_with_asterisk",
  "SPI": "default_spi_formula",
  "spi_name": "SPI",
  "cpi_name": "CPI"
}'),

-- 2. Grade Upload API
('Grade Upload API', '/upload-grades',
'Uploads a CSV or Excel file containing student grades. The file should follow the specified format, including student IDs, course codes, and corresponding grades.',
'{
  "grades_uploaded": [
    {
      "roll_number": "2024001",
      "course_code": "CS102",
      "grade": "AA",
      "grade_type": "initial",
      "semester": "Monsoon",
      "academic_year": "2023-2024",
      "elective_change": "no",
      "new_course_code": null,
      "previous_course_id": null
    },
    {
      "roll_number": "2024003",
      "course_code": "CS105",
      "grade": "CD",
      "grade_type": "repeat",
      "semester": "Winter",
      "academic_year": "2023-2024",
      "elective_change": "yes",
      "new_course_code": "CS105",
      "previous_course_id": "CS104"
    }
  ]
}');

INSERT INTO Grade_Types (type_name) VALUES
('initial'),
('repeat');


INSERT INTO SPI_Formula (formula_name, formula) VALUES
('default_spi_formula', 'sum(semester_course_credits * semester_grade_value) / sum(semester_course_credits)');

INSERT INTO CPI_Formula (formula_name, formula) VALUES
('default_cpi_formula', 'sum(total_course_credits * grade_value) / sum(total_course_credits)');

INSERT INTO Actions (action_type) VALUES
('Set Grading System'),
('Uploaded Grades'),
('Set PDF Description'),
('Updated Grading System'),
('Changed Employee Roles');

DELIMITER //

CREATE TRIGGER encrypt_password_before_insert_student
BEFORE INSERT ON Students
FOR EACH ROW
BEGIN
    SET NEW.password = AES_ENCRYPT(NEW.password, 'super_secret_key@12345!');
END//

DELIMITER ;

DELIMITER //

CREATE TRIGGER encrypt_password_before_update_student
BEFORE UPDATE ON Students
FOR EACH ROW
BEGIN
    IF NEW.password != OLD.password THEN
        SET NEW.password = AES_ENCRYPT(NEW.password, 'super_secret_key@12345!');
    END IF;
END//

DELIMITER ;


DELIMITER //

CREATE TRIGGER encrypt_password_before_insert_employee
BEFORE INSERT ON Employees
FOR EACH ROW
BEGIN
    SET NEW.password = AES_ENCRYPT(NEW.password, 'super_secret_key@12345!');
END//

DELIMITER ;

DELIMITER //

CREATE TRIGGER encrypt_password_before_update_employee
BEFORE UPDATE ON Employees
FOR EACH ROW
BEGIN
    IF NEW.password != OLD.password THEN
        SET NEW.password = AES_ENCRYPT(NEW.password, 'super_secret_key@12345!');
    END IF;
END//

DELIMITER ;