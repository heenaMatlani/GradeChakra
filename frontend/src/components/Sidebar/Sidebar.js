import React from 'react';
import { Link } from 'react-router-dom'; // Import Link
import './Sidebar.css';

const Sidebar = ({ userType }) => {
  return (
    <div className="sidebar">
      <ul>
        {userType === 'student' && (
          <>
            <li><Link to="/student/profile"><i className="icon fas fa-user"></i>My Profile</Link></li>
            <li><Link to="/student"><i className="icon fas fa-graduation-cap"></i>My Grades</Link></li>
            <li><Link to="/student/overall-results"><i className="icon fas fa-chart-line"></i>Overall Results</Link></li>
            <li><Link to="/student/report-issue"><i className="icon fas fa-exclamation-circle"></i>Report an Issue</Link></li>
          </>
        )}
        {userType === 'faculty' && (
          <>
            <li><Link to="/faculty/profile"><i className="icon fas fa-user"></i>My Profile</Link></li>
            <li><Link to="/faculty/courses"><i className="icon fas fa-book"></i>My Courses</Link></li>
            <li><Link to="/faculty"><i className="icon fas fa-graduation-cap"></i>Course-wise Results</Link></li>
            <li><Link to="/faculty/overall-performance"><i className="icon fas fa-chart-line"></i>Overall Performance</Link></li>
            <li><Link to="/faculty/grade-change-request"><i className="icon fas fa-exclamation-circle"></i>Grade Change Request</Link></li>
          </>
        )}
        {userType === 'admin' && (
          <>
            <li><Link to="/admin/profile"><i className="icon fas fa-user"></i>My Profile</Link></li>
            <li><Link to="/admin"><i className="icon fas fa-tachometer-alt"></i>Dashboard</Link></li>
            <li><Link to="/admin/grading-config"><i className="icon fas fa-graduation-cap"></i>Grading System</Link></li>
            <li><Link to="/admin/pdf-config"><i className="icon fas fa-file-pdf"></i>Handle Report PDFs</Link></li>
            <li><Link to="/admin/logs"><i className="icon fas fa-file-alt"></i>View Logs</Link></li>
          </>
        )}
        {userType === 'staff' && (
          <>
            <li><Link to="/staff/profile"><i className="icon fas fa-user"></i>My Profile</Link></li>
            <li><Link to="/staff"><i className="icon fas fa-tachometer-alt"></i>Dashboard</Link></li>
            <li><Link to="/staff/grades"><i className="icon fas fa-graduation-cap"></i>Manage Grades</Link></li>
            <li><Link to="/staff/search-grades"><i className="icon fas fa-search"></i>Search Grades</Link></li>
            <li><Link to="/staff/student-issues"><i className="icon fas fa-exclamation-circle"></i>Student Issues</Link></li>
            <li><Link to="/staff/faculty-requests"><i className="icon fas fa-envelope"></i>Faculty Requests</Link></li>
          </>
        )}
      </ul>
    </div>
  );
};

export default Sidebar;
