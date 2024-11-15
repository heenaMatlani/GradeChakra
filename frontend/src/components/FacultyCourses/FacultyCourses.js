import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './FacultyCourses.css';

const FacultyCourses = ({ userEmail }) => {
  const [courses, setCourses] = useState([]);
  const [expandedCourse, setExpandedCourse] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!userEmail) {
      setError("Session expired. Please log in again.");
      return;
    }

    const fetchCourses = async () => {
      try {
        const response = await axios.get('/faculty/courses-expanded', { params: { userEmail } });
        setCourses(response.data);
      } catch (error) {
        setError(error.response?.data.message || "Failed to fetch courses.");
      }
    };

    fetchCourses();
  }, [userEmail]);

  const toggleCourseDetails = (index) => {
    setExpandedCourse(expandedCourse === index ? null : index);
  };

  const handleDownload = (courseId, semesterId, academicYear) => {
    axios.get(`/faculty/download-course-grades`, {
      params: { course_id: courseId, semester_id: semesterId, academic_year: academicYear },
      responseType: 'blob'
    })
    .then(response => {
      const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = response.headers['content-disposition']?.split('filename=')[1] || `Course_Grades_${semesterId}.xlsx`;
      link.click();
    })
    .catch(error => console.error("Error downloading file:", error));
  };

  return (
    <div className="faculty-courses-container">
      <h2>My Courses</h2>
      {error ? (
        <p>{error}</p>
      ) : (
        <table className="courses-table">
          <thead>
            <tr>
              <th>Details</th>
              <th>Course Code</th>
              <th>Course Name</th>
            </tr>
          </thead>
          <tbody>
            {courses.map((course, index) => (
              <React.Fragment key={index}>
                <tr>
                  <td>
                    <button className="expand-button" onClick={() => toggleCourseDetails(index)}>
                      <span className={`arrow ${expandedCourse === index ? 'open' : ''}`}>
                        {expandedCourse === index ? '▼' : '▶'}
                      </span>
                    </button>
                  </td>
                  <td>{course.code}</td>
                  <td>{course.name}</td>
                </tr>
                {expandedCourse === index && (
                  <tr className="course-details-row">
                    <td colSpan="3">
                      <div className="course-details">
                        {course.semesters.map((sem, i) => (
                          <React.Fragment key={i}>
                            <div className="semester-info">
                              <h4>{sem.semester} - {sem.academic_year}</h4>
                              <button
                                className="download-button"
                                onClick={() => handleDownload(course.course_id, sem.semester_id, sem.academic_year.split('-')[0])}>
                                View Course Result
                              </button>
                            </div>
                            {i < course.semesters.length - 1 && <hr className="separator" />}
                          </React.Fragment>
                        ))}
                      </div>
                    </td>
                  </tr>
                )}
              </React.Fragment>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default FacultyCourses;
