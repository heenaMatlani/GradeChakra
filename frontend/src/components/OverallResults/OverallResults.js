import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './OverallResults.css';
import BarChart from '../BarChart/BarChart';

const OverallResults = ({ userEmail, userType }) => {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!userEmail) {
      setError("Session expired. Please log in again.");
      setLoading(false);
      return;
    }

    const fetchOverallResults = async () => {
      try {
        const endpoint = userType === 'student' ? '/student/overall-results' : '/faculty/grade-distribution';
        const response = await axios.get(endpoint, { params: { userEmail } });
        setResults(response.data);
      } catch (error) {
        setError(error.response?.data.message || 'Failed to fetch overall results');
      } finally {
        setLoading(false);
      }
    };

    fetchOverallResults();
  }, [userEmail, userType]);

  return (
    <div className="overall-results-container">
      <h1>{userType === 'student' ? 'Your Overall Results' : 'Grade Distribution by Subject'}</h1>
      {loading ? (
        <p>Loading...</p>
      ) : error || !results ? (
        <div className="no-results-message">
          <p>{error || "No results available"}</p>
        </div>
      ) : (
        userType === 'student' ? (
          <StudentResults results={results} />
        ) : (
          <FacultyResults results={results} />
        )
      )}
    </div>
  );
};

const StudentResults = ({ results }) => {
  return (
    <div className="student-results">
      <table>
        <thead>
          <tr>
            <th>Semester</th>
            <th>SPI</th>
          </tr>
        </thead>
        <tbody>
          {results.semesters.map((semester, index) => (
            <tr key={index}>
              <td>{semester.name}</td>
              <td>{semester.spi}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <h3 className="cpi">
        CPI: <span className="cpi-value">{results.cpi}</span>
      </h3>
    </div>
  );
};

const FacultyResults = ({ results }) => {
  return (
    <div className="faculty-results chart-row">
      {results.map((subject, index) => (
        <div className="chart-column" key={index}>
          <BarChart grades={subject.grades} />
          <h3>{subject.course_code}: {subject.course_name}</h3>
          <p className="semester-info">{subject.semester} {subject.academic_year}</p>
        </div>
      ))}
    </div>
  );
};

export default OverallResults;
