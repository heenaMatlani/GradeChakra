import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import './ResultsTable.css';

const ResultsTable = () => {
  const location = useLocation();
  const { course } = location.state; // Retrieve course data passed from the FacultyDashboard
  const [grades, setGrades] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchGrades = async () => {
      try {
        const response = await axios.get('/faculty/course-grades', {
          params: {
            course_id: course.course_id,
            semester_id: course.semester_id,
            academic_year: course.academic_year.split("-")[0],
          },
        });
        setGrades(response.data.grades);
      } catch (error) {
        setError(error.response?.data.message || "Failed to fetch course grades.");
      }
    };

    fetchGrades();
  }, [course]);

  const handleDownload = async () => {
    try {
      const response = await axios.get('/faculty/download-course-grades', {
        params: {
          course_id: course.course_id,
          semester_id: course.semester_id,
          academic_year: course.academic_year.split("-")[0],
        },
        responseType: 'blob',
      });
      const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = `${course.code}_${course.semester}_${course.academic_year}.xlsx`;
      link.click();
      URL.revokeObjectURL(link.href);
    } catch (error) {
      console.error('Error downloading grades:', error);
    }
  };

  return (
    <div className="course-grades-page">
      <h2>Grades for {course.code} ({course.semester} {course.academic_year})</h2>
      {error ? (
        <p>{error}</p>
      ) : (
        <>
          <div className="course-grades-table-container">
            <table className="course-grades-table">
              <thead>
                <tr>
                  <th>Roll Number</th>
                  <th>Student Name</th>
                  <th>Grade</th>
                  <th>Grade Type</th>
                </tr>
              </thead>
              <tbody>
                {grades.map((grade, index) => (
                  <tr key={index}>
                    <td>{grade.roll_number}</td>
                    <td>{grade.student_name}</td>
                    <td>{grade.grade}</td>
                    <td>{grade.grade_type}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="results-button">
          <button className="result-download-button" onClick={handleDownload}>
            Download Excel
          </button>

          </div>
        </>
      )}
    </div>
  );
};

export default ResultsTable;
