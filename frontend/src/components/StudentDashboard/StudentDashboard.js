import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './StudentDashboard.css';
import Card from '../Card/Card';

const StudentDashboard = ({ userEmail }) => {
  const [semesters, setSemesters] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!userEmail) {
      setError("Session expired. Please log in again.");
      setLoading(false);
      return;
    }

    const fetchSemesters = async () => {
      try {
        const response = await axios.get(`/student/grade-reports`, {
          params: { userEmail }
        });
        setSemesters(response.data);
      } catch (error) {
        setError(error.response?.data.message || 'Failed to fetch reports');
      } finally {
        setLoading(false);
      }
    };

    fetchSemesters();
  }, [userEmail]);

  const handleDownload = async (semesterId) => {
    try {
      const response = await axios.get(`/download-grade-pdf`, {
        params: { userEmail, semesterId },
        responseType: 'blob'
      });
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = response.headers['content-disposition']?.split('filename=')[1] || `Semester_${semesterId}_Grade_Report.pdf`;
      link.click();
      URL.revokeObjectURL(link.href);
    } catch (error) {
      console.error('Error downloading PDF:', error);
    }
  };

  return (
    <div className="student-dashboard">
      <h2>Results</h2>
      {loading ? (
        <p>Loading...</p>
      ) : error || semesters.length === 0 ? (
        <div className="no-results-message">
          <p>{error || "No results available"}</p>
        </div>      ) : (
        <div className="cards-container">
          {semesters.map((semester, index) => (
            <Card
              key={index}
              title={semester.semester}
              buttonText="Download Grade PDF"
              onButtonClick={() => handleDownload(semester.semester_id)}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default StudentDashboard;
