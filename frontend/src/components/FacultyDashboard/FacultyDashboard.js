import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './FacultyDashboard.css';
import Card from '../Card/Card';
import ResultsTable from '../ResultsTable/ResultsTable';
import { useNavigate } from 'react-router-dom';


const FacultyDashboard = ({ userEmail }) => {
  const [courses, setCourses] = useState([]);
  const [filteredCourses, setFilteredCourses] = useState([]);
  const [startYear, setStartYear] = useState('');
  const [endYear, setEndYear] = useState('');
  const [semesterFilter, setSemesterFilter] = useState('');
  const [courseCodeFilter, setCourseCodeFilter] = useState('');
  const [showFilter, setShowFilter] = useState(false);
  const [error, setError] = useState('');
  const [filterOptions, setFilterOptions] = useState({ course_codes: [], semesters: [] });
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [courseGrades, setCourseGrades] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();


  useEffect(() => {
    if (!userEmail) {
      setError("Session expired. Please log in again.");
      return;
    }

    const fetchCourses = async () => {
      try {
        const response = await axios.get('/faculty/courses', { params: { userEmail } });
        setCourses(response.data);
        setFilteredCourses(response.data);
      } catch (error) {
        setError(error.response?.data.message || "Failed to fetch courses.");
      }
    };

    const fetchFilterOptions = async () => {
      try {
        const response = await axios.get('/faculty/filter-options', { params: { userEmail } });
        setFilterOptions(response.data);
      } catch (error) {
        console.error("Error fetching filter options:", error);
      }
    };

    fetchCourses();
    fetchFilterOptions();
  }, [userEmail]);

  const handleFilter = () => {
    let filtered = courses;

    if (startYear && endYear) {
      filtered = filtered.filter(course =>
        course.academic_year >= startYear && course.academic_year <= endYear
      );
    }

    if (semesterFilter) {
      filtered = filtered.filter(course => course.semester === semesterFilter);
    }

    if (courseCodeFilter) {
      filtered = filtered.filter(course => course.code === courseCodeFilter);
    }

    setFilteredCourses(filtered);
  };

  const toggleFilter = () => {
    setShowFilter(!showFilter);
  };

  const handleViewGrades = (course) => {
    navigate(`/faculty/course-grades`, {
      state: { course },
    });
  };




  return (
    <div className="faculty-dashboard">
      <h2>Course Results</h2>
      {error ? (
        <p>{error}</p>
      ) : (
        <>
          <div className="top-bar">
            <button onClick={toggleFilter} className="filter-toggle-button">
              <div className="filter-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="currentColor" class="bi bi-filter" viewBox="0 0 16 16">
                  <path d="M6 10.5a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5m-2-3a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5m-2-3a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 0 1h-11a.5.5 0 0 1-.5-.5"/>
                </svg>
                </div>
              {showFilter ? 'Hide Filter' : 'Show Filter'}
            </button>
          </div>

          {showFilter && (
            <div className="filter-container">
              <div className="filter-row">
                <label>Start Year:</label>
                <input
                  type="text"
                  placeholder="YYYY"
                  value={startYear}
                  onChange={(e) => setStartYear(e.target.value)}
                />
                <label>End Year:</label>
                <input
                  type="text"
                  placeholder="YYYY"
                  value={endYear}
                  onChange={(e) => setEndYear(e.target.value)}
                />

                <label>Semester:</label>
                <select value={semesterFilter} onChange={(e) => setSemesterFilter(e.target.value)}>
                  <option value="">Select Semester</option>
                  {filterOptions.semesters.map((semester, index) => (
                    <option key={index} value={semester}>{semester}</option>
                  ))}
                </select>

                <label>Course Code:</label>
                <select value={courseCodeFilter} onChange={(e) => setCourseCodeFilter(e.target.value)}>
                  <option value="">Select Course Code</option>
                  {filterOptions.course_codes.map((code, index) => (
                    <option key={index} value={code}>{code}</option>
                  ))}
                </select>
              </div>
        <div className="apply-filter-row">
          <button onClick={handleFilter} className="apply-filter-button">Apply Filter</button>
        </div>

                    </div>
          )}

          <div className="cards-container">
            {filteredCourses.length > 0 ? (
              filteredCourses.map((course, index) => (
                <Card
                  key={index}
                  title={course.code}
                    description={
                      <>
                        {course.description}
                        <br />
                        {course.semester} {course.academic_year}
                      </>
                    }
                buttonText="View All Student Grades"
              onButtonClick={() => handleViewGrades(course)}
                />
              ))
            ) : (
              <p>No courses available.</p>
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default FacultyDashboard;
