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

## Installation

### Prerequisites
Ensure the following are installed on your system:
- **Python** (3.8 or later)
- **Node.js** (for React)
- **MySQL**

### Backend Installation (Flask)
1. Clone the repository:
   ```bash
   git clone https://github.com/heenaMatlani/GradeChakra
   cd backend
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install Flask mysql-connector-python
   ```

4. Set up `config.py` file for database configurations:
   ```env
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_password
   ```

5. Initialize the database:
   - Run `queries.sql` to create all necessary tables:
     ```bash
     mysql -u root -p GradeManagementSystem < queries.sql
     ```
   - Run `dummydata.sql` to populate dummy data:
     ```bash
     mysql -u root -p GradeManagementSystem < dummydata.sql
     ```

6. Start the Flask server:
   ```bash
   flask run
   ```

### Frontend Installation (React)
1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the React development server:
   ```bash
   npm start
   ```

---

### Starting the Application
- Backend runs on `http://127.0.0.1:5000`
- Frontend runs on `http://127.0.0.1:3000`

---

## Technologies Used

### Backend
- **Flask**: Web framework
- **MySQL**: Database
- **mysql-connector-python**: Database connectivity
- **reportlab**: PDF generation library

### Frontend
- **React**: Frontend framework
- **Axios**: For API calls

---

## Contributing
1. Fork the repository.
2. Create a new branch for your feature:
   ```bash
   git checkout -b feature-name
   ```
3. Commit and push your changes:
   ```bash
   git commit -m "Description of changes"
   git push origin feature-name
   ```
4. Submit a pull request.

---

## Contact
For queries or support, contact **Heena Matlani** at [heenamatlani07@gmail.com].
