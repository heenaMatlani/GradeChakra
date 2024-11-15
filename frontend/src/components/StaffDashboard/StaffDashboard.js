import React from 'react';
import Card from '../Card/Card';
import './StaffDashboard.css';

const StaffDashboard = () => {
  return (
    <div className="staff-dashboard">
      <h1>Staff Dashboard</h1>
      <div className="staff-card-container">
        <Card
          title="Profile"
          description="View and update your personal profile details."
          buttonText="View Profile"
          onButtonClick={() => window.location.href='/staff/profile'}
        />
        <Card
          title="Upload Grades"
          description="Upload or update student grades using an Excel sheet or online forms."
          buttonText="Upload Now"
          onButtonClick={() => window.location.href='/staff/upload-grades'}
        />
        <Card
          title="Grade Queries"
          description="Retrieve data insights of grades by querying student, batch, course, and other grade information."
          buttonText="Search Now"
          onButtonClick={() => window.location.href='/staff/search-grades'}
        />
        <Card
          title="Student Issues"
          description="View issues submitted by students regarding their grade reports."
          buttonText="View Issues"
          onButtonClick={() => window.location.href='/staff/student-issues'}
        />
        <Card
          title="Faculty Requests"
          description="Review faculty requests to modify grades or make adjustments to course grades."
          buttonText="Review Requests"
          onButtonClick={() => window.location.href='/staff/faculty-requests'}
        />
      </div>
    </div>
  );
};

export default StaffDashboard;
