# Grade Management System  

The **Grade Management System** is a dynamic, configurable platform designed to streamline the grading process for educational institutions. It empowers institutions to define and manage grading rules, calculate SPI/CPI, handle course repetitions, and generate grade reports automatically while ensuring security and adaptability to different academic systems.  

---

## Features  

### Configurable Grading System  
- Define grading rules, including grading scales, SPI/CPI formulas, and grade replacement policies.  
- Support for multiple grading systems for different batches, preserving historical grading policies.  

### Role-Based Interfaces  
- **Administrators**: Configure grading rules and policies.  
- **Academic Staff**: Upload grades, handle grade updates, and manage records.  
- **Faculty Members**: Access grades for courses they teach.  
- **Students**: View grades, download PDF grade reports, and receive notifications.  

### Automated and Secure Grade Reporting  
- Dynamic PDF generation for student grade reports, customized for institutional requirements.  
- Downloadable Excel reports for faculty and administrators.  

### Robust Security  
- AES-encrypted database storage for sensitive data.  
- JWT-based authentication and role-based access control.  
- Comprehensive audit logging to ensure accountability.  

### Error Handling and Input Validation  
- Strict validation for inputs, including grades, course registrations, and grading rules.  
- Automated error detection and user notifications for failed operations.  

---

## Project Structure  

GradeManagementSystem/
├── backend/
│ ├── app.py
│ ├── routes/
│ │ ├── admin.py
│ │ ├── grades.py
│ │ ├── faculty.py
│ │ ├── students.py
│ └── services/
│ ├── grading_system_service.py
│ ├── pdfGenerationService.py
│ ├── calculate_spi_cpi.py
├── frontend/
│ ├── public/
│ │ ├── index.html
│ │ └── favicon.ico
│ ├── src/
│ │ ├── components/
│ │ │ ├── FacultyDashboard.js
│ │ │ ├── StudentDashboard.js
│ │ │ ├── ResultsTable.js
│ │ ├── styles/
│ │ │ ├── FacultyDashboard.css
│ │ │ ├── ResultsTable.css
│ │ │ ├── App.css
│ ├── App.js
│ ├── index.js
│ └── package.json
└── README.md


---

## Installation  

### Prerequisites  
- **Backend**: Python 3.10+, Flask, Flask-CORS, MySQL, ReportLab, Pandas, Pytest  
- **Frontend**: Node.js, React.js  

### Setup  

1. **Clone the Repository**  
   ```bash  
   git clone https://github.com/your-username/GradeManagementSystem.git  
   cd GradeManagementSystem  
Backend

Navigate to the backend folder:
bash
Copy code
cd backend  
Create a virtual environment and activate it:
bash
Copy code
python3 -m venv venv  
source venv/bin/activate  # Linux/Mac  
venv\Scripts\activate     # Windows  
Install dependencies:
bash
Copy code
pip install -r requirements.txt  
Set up the database (MySQL):
sql
Copy code
CREATE DATABASE GradeManagement;  
Import the database schema from schema.sql.
Run the backend server:
bash
Copy code
python app.py  
Frontend

Navigate to the frontend folder:
bash
Copy code
cd ../frontend  
Install dependencies:
bash
Copy code
npm install  
Start the React development server:
bash
Copy code
npm start  
API Endpoints
Authentication
POST /login – Authenticate users and generate JWT tokens.
Grading Rules Management
POST /admin/grading-rules – Add new grading rules.
GET /admin/grading-rules – Retrieve all grading rules.
Grade Upload and Management
POST /grades/upload – Upload grades via Excel or JSON.
GET /grades/student-report – Generate and download student PDF grade reports.
GET /grades/faculty-report – Retrieve grades for faculty-specific course
