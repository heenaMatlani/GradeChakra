import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import StudentDashboard from './components/StudentDashboard/StudentDashboard';
import FacultyDashboard from './components/FacultyDashboard/FacultyDashboard';
import AdminDashboard from './components/AdminDashboard/AdminDashboard';
import StaffDashboard from './components/StaffDashboard/StaffDashboard';
import FacultyCourses from './components/FacultyCourses/FacultyCourses';
import GradeCommunication from './components/GradeCommunication/GradeCommunication';
import Layout from './components/Layout/Layout';
import Login from './components/Login/Login';
import Profile from './components/Profile/Profile';
import ViewLogs from './components/ViewLogs/ViewLogs';
import OverallResults from './components/OverallResults/OverallResults';
import GradingConfig from './components/GradingConfig/GradingConfig';
import PdfConfig from './components/PdfConfig/PdfConfig';
import EmployeeRolesManagement from './components/EmployeeRolesManagement/EmployeeRolesManagement.js';
import HandleGrades from './components/HandleGrades/HandleGrades';
import SearchGrades from './components/SearchGrades/SearchGrades';
import ProtectedRoute from './components/ProtectedRoute/ProtectedRoute';
import Messages from './components/Messages/Messages';
import ResultsTable from './components/ResultsTable/ResultsTable';

const App = () => {
  const studentData = {
    name: 'Heena Matlani',
    rollNo: '2101082',
    batch: '2021',
    program: 'BTech',
    department: 'Computer Science',
    email: 'heena.matlani@iiitg.ac.in',
  };

  const facultyData = {
    name: 'Dr. Gautam Barua',
    department: 'Computer Science',
    email: 'gautam.barua@iiitg.ac.in',
    role: 'HOD',
    startDate: '2019-08-01',
  };

  const results = {
    semesters: [
      { name: 'Semester 1', spi: 8.29 },
      { name: 'Semester 2', spi: 8.95 },
      { name: 'Semester 3', spi: 9.10 },
    ],
    cpi: 8.78,
  };

  const facultyResults = {
    "subjects": [
      {
        "code": "CS104",
        "name": "Operating Systems",
        "grades": {"AA": 12, "AB": 23, "BB": 10}
      },
      {
        "code": "CS105",
        "name": "Database Management Systems",
        "grades": {"AA": 10, "AB": 20, "BB": 15}
      }
    ]
  };

  // Assuming you will manage authentication state
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userType, setUserType] = useState('');
  const [userName, setUserName] = useState(''); // For displaying in Navbar
  const [userEmail, setUserEmail] = useState('')

  // Simulate user login for demonstration
  useEffect(() => {
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('userData');

    if (token && userData) {
      setIsLoggedIn(true);
      const parsedUserData = JSON.parse(userData);
      setUserType(parsedUserData.userType);
      setUserName(parsedUserData.userName);
      setUserEmail(parsedUserData.email);
    } else {
      setIsLoggedIn(false);
      setUserType('');
      setUserName('');
      setUserEmail('');
    }
  }, []);
// Add an empty dependency array to run this effect only once when the component mounts


  return (
    <Router>
      <Routes>
        <Route path="/login" element={
        <Login
            setIsLoggedIn={setIsLoggedIn}
            setUserType={setUserType}
            setUserName={setUserName}
            setUserEmail={setUserEmail}
        />}
        />

        <Route element={<Layout isLoggedIn={isLoggedIn} userType={userType} userName={userName}/>}>
          <Route
            path="/student"
            element={
              <ProtectedRoute isLoggedIn={isLoggedIn} userType={userType} requiredUserType="student">
                <StudentDashboard userEmail={userEmail}/>
              </ProtectedRoute>
            }
          />
          <Route
            path="/student/profile"
            element={
              <ProtectedRoute isLoggedIn={isLoggedIn} userType={userType} requiredUserType="student">
                <Profile userType="student" userDetails={studentData} userEmail={userEmail}/>
              </ProtectedRoute>
            }
          />
          <Route
            path="/student/overall-results"
            element={
              <ProtectedRoute isLoggedIn={isLoggedIn} userType={userType} requiredUserType="student">
                <OverallResults userType="student" userEmail={userEmail} />
              </ProtectedRoute>
            }
          />
          <Route
            path="/student/report-issue"
            element={
              <ProtectedRoute isLoggedIn={isLoggedIn} userType={userType} requiredUserType="student">
                <GradeCommunication userType={userType} userEmail={userEmail} />
              </ProtectedRoute>
            }
          />

          <Route
            path="/faculty"
            element={
              <ProtectedRoute isLoggedIn={isLoggedIn} userType={userType} requiredUserType="faculty">
                <FacultyDashboard userEmail={userEmail}/>
              </ProtectedRoute>
            }
          />
          <Route
            path="/faculty/profile"
            element={
              <ProtectedRoute isLoggedIn={isLoggedIn} userType={userType} requiredUserType="faculty">
                <Profile userType="faculty" userDetails={facultyData} userEmail={userEmail} />
              </ProtectedRoute>
            }
          />
          <Route
            path="/faculty/courses"
            element={
              <ProtectedRoute isLoggedIn={isLoggedIn} userType={userType} requiredUserType="faculty">
                <FacultyCourses userEmail={userEmail}/>
              </ProtectedRoute>
            }
          />
          <Route
            path="/faculty/overall-performance"
            element={
              <ProtectedRoute isLoggedIn={isLoggedIn} userType={userType} requiredUserType="faculty">
                <OverallResults userType="faculty" userEmail={userEmail} />
              </ProtectedRoute>
            }
          />
          <Route
            path="/faculty/course-grades"
            element={
              <ProtectedRoute isLoggedIn={isLoggedIn} userType={userType} requiredUserType="faculty">
                <ResultsTable />
              </ProtectedRoute>
            }
          />
          <Route
            path="/faculty/grade-change-request"
            element={
              <ProtectedRoute isLoggedIn={isLoggedIn} userType={userType} userEmail={userEmail} requiredUserType="faculty">
                <GradeCommunication userType={userType} userEmail={userEmail} />
              </ProtectedRoute>
            }
          />

          <Route
            path="/admin"
            element={
              <ProtectedRoute isLoggedIn={isLoggedIn} userType={userType} requiredUserType="admin">
                <AdminDashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin/profile"
            element={
              <ProtectedRoute isLoggedIn={isLoggedIn} userType={userType} requiredUserType="admin">
                <Profile userType="admin" userDetails={facultyData} userEmail={userEmail} />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin/grading-config"
            element={
              <ProtectedRoute isLoggedIn={isLoggedIn} userType={userType} requiredUserType="admin">
                <GradingConfig />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin/pdf-config"
            element={
              <ProtectedRoute isLoggedIn={isLoggedIn} userType={userType} requiredUserType="admin">
                <PdfConfig />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin/employee-role-management"
            element={
              <ProtectedRoute isLoggedIn={isLoggedIn} userType={userType} requiredUserType="admin">
                <EmployeeRolesManagement />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin/logs"
            element={
              <ProtectedRoute isLoggedIn={isLoggedIn} userType={userType} requiredUserType="admin">
                <ViewLogs />
              </ProtectedRoute>
            }
          />

          <Route
            path="/staff"
            element={
              <ProtectedRoute isLoggedIn={isLoggedIn} userType={userType} requiredUserType="staff">
                <StaffDashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/staff/profile"
            element={
              <ProtectedRoute isLoggedIn={isLoggedIn} userType={userType} requiredUserType="staff">
                <Profile userType="staff" userDetails={facultyData} userEmail={userEmail} />
              </ProtectedRoute>
            }
          />
          <Route
            path="/staff/grades"
            element={
              <ProtectedRoute isLoggedIn={isLoggedIn} userType={userType} requiredUserType="staff">
                <HandleGrades />
              </ProtectedRoute>
            }
          />
          <Route
            path="/staff/search-grades"
            element={
              <ProtectedRoute isLoggedIn={isLoggedIn} userType={userType} requiredUserType="staff">
                <SearchGrades />
              </ProtectedRoute>
            }
          />
          <Route
            path="/staff/student-issues"
            element={
              <ProtectedRoute isLoggedIn={isLoggedIn} userType={userType} requiredUserType="staff">
                <Messages messageType="student" />
              </ProtectedRoute>
            }
          />
          <Route
            path="/staff/faculty-requests"
            element={
              <ProtectedRoute isLoggedIn={isLoggedIn} userType={userType} requiredUserType="staff">
                <Messages messageType="faculty" />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<Navigate to="/login" />} />
        </Route>
      </Routes>
    </Router>
  );
};

export default App;




