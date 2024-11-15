import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './SearchGrades.css';
import BarChart from '../BarChart/BarChart';

const SearchGrades = () => {
  const [batchYear, setBatchYear] = useState('');
  const [rollNumber, setRollNumber] = useState('');
  const [programs, setPrograms] = useState([]);
  const [program, setProgram] = useState('');
  const [department, setDepartment] = useState('');
  const [courseCode, setCourseCode] = useState('');
  const [semesterName, setSemesterName] = useState('');
  const [academicYear, setAcademicYear] = useState('');
  const [metric, setMetric] = useState('cpi');
  const [customQuery, setCustomQuery] = useState('');
  const [availableDepartments, setAvailableDepartments] = useState([]);
  const [availableSemesters, setAvailableSemesters] = useState([]);
  const [gradeView, setGradeView] = useState('whole');
const [grades, setGrades] = useState({});

  useEffect(() => {
    axios.get('/search-grades/filter-options')
      .then(response => {
        setPrograms(response.data.programs);
        setAvailableDepartments(response.data.departments);
        setAvailableSemesters(response.data.semesters);
      })
      .catch(error => console.error('Error fetching filter options:', error));
  }, []);

const downloadFile = (response, filename) => {
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', filename);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link); // Clean up
  window.URL.revokeObjectURL(url);
};



const handleStudentReportDownload = () => {
  if (!rollNumber) {
    alert("Please enter a valid roll number.");
    return;
  }

  axios.get('/search-grades/student/report', {
      params: { roll_number: rollNumber },
      responseType: 'blob'
    })
    .then(response => downloadFile(response, `${rollNumber}_Report.pdf`))
    .catch(error => console.error('Error downloading student report:', error));
};

const handleBatchSpiCpiDownload = () => {
  if (!batchYear || !program) {
    alert("Please enter the batch year and select a program.");
    return;
  }

  axios.get('/search-grades/batch/spi_cpi', {
      params: { batch_year: batchYear, program },
      responseType: 'blob'
    })
    .then(response => downloadFile(response, `Batch_${batchYear}_SPI_CPI_Report.xlsx`))
    .catch(error => console.error('Error downloading SPI and CPI report:', error));
};



  const handleBatchCpiDownload = () => {
    axios.get('/search-grades/batch/cpi', { params: { batch_year: batchYear, program },responseType: 'blob' })
      .then(response => downloadFile(response, `Batch_${batchYear}_CPI_Report.xlsx`))
      .catch(error => console.error('Error downloading CPI report:', error));
  };


  const handleBatchDepartmentCpiDownload = () => {
    axios.get('/search-grades/batch-department/cpi', { params: { batch_year: batchYear, program, department },responseType: 'blob' })
      .then(response => downloadFile(response, `Batch_${batchYear}_${department}_CPI_Report.xlsx`))
      .catch(error => console.error('Error downloading batch & department CPI report:', error));
  };

  const handleBatchDepartmentSpiCpiDownload = () => {
    axios.get('/search-grades/batch-department/spi_cpi', { params: { batch_year: batchYear, program, department },responseType: 'blob' })
      .then(response => downloadFile(response, `Batch_${batchYear}_${department}_SPI_CPI_Report.xlsx`))
      .catch(error => console.error('Error downloading batch & department SPI/CPI report:', error));
  };

  const handleCourseGradesDownload = () => {
    axios.get('/search-grades/course/grades', { params: { course_code: courseCode, semester_name: semesterName, academic_year: academicYear },responseType: 'blob' })
      .then(response => downloadFile(response, `${courseCode}_${semesterName}_${academicYear}_Grades.xlsx`))
      .catch(error => console.error('Error downloading course grades:', error));
  };

  const handleStatisticsCalculation = () => {
    axios.get('/search-grades/statistics', { params: { metric, batch_year: batchYear, program, department, semester: semesterName, course_code: courseCode },responseType: 'blob' })
      .then(response => {
        console.log('Statistics:', response.data);
      })
      .catch(error => console.error('Error calculating statistics:', error));
  };

const handleGradeDistributionFetch = () => {
  axios.get('/search-grades/grade-distribution', {
    params: { semester_name: semesterName, academic_year: academicYear, batch_year: batchYear, program, department, grade_view: gradeView },
  })
    .then(response => {
      const gradesData = response.data.reduce((acc, item) => {
        acc[item.grade] = item.count; // Map grades to counts
        return acc;
      }, {});
      setGrades(gradesData); // Update state to pass to the chart
    })
    .catch(error => console.error('Error fetching grade distribution:', error));
};


  const handleCustomQueryDownload = () => {
    axios.get('/search-grades/custom-query', { params: { query: customQuery },responseType: 'blob' })
      .then(response => downloadFile(response, 'Custom_Query_Results.csv'))
      .catch(error => console.error('Error executing custom query:', error));
  };

  return (
    <div className="search-grades">
      <h1>Grade Queries</h1>

      {/* Student PDF Report */}
      <div className="card">
        <h2>Search student and download PDF report</h2>
        <p>Download an individual student’s PDF report by searching their details.</p>
        <input type="text" placeholder="Enter Student Roll number" value={rollNumber} onChange={(e) => setRollNumber(e.target.value)} />
        <button className="download-button" onClick={handleStudentReportDownload}>Download PDF</button>
      </div>

      {/* Batch CPI Download */}
      <div className="card">
        <h2>Download CPI sheet for entire batch</h2>
        <p>Download an Excel sheet for a batch with CPI, roll number, and name.</p>
        <input type="text" placeholder="Enter Batch Year (e.g., 2021)" value={batchYear} onChange={(e) => setBatchYear(e.target.value)} />
        <select value={program} onChange={(e) => setProgram(e.target.value)}>
          <option value="">Select Program</option>
          {programs.map((prog, index) => <option key={index} value={prog}>{prog}</option>)}
        </select>
        <button className="download-button" onClick={handleBatchCpiDownload}>Download Excel</button>
      </div>

      {/* Batch SPI & CPI Download */}
      <div className="card">
        <h2>Download SPI & CPI sheet for entire batch</h2>
        <p>Download an Excel sheet for a batch with SPI for each semester, CPI (till that semester), roll number, and name.</p>
        <input type="text" placeholder="Enter Batch Year (e.g., 2021)" value={batchYear} onChange={(e) => setBatchYear(e.target.value)} />
        <select value={program} onChange={(e) => setProgram(e.target.value)}>
          <option value="">Select Program</option>
          {programs.map((prog, index) => <option key={index} value={prog}>{prog}</option>)}
        </select>
        <button className="download-button" onClick={handleBatchSpiCpiDownload}>Download Excel</button>
      </div>

      {/* Batch & Department CPI Download */}
      <div className="card">
        <h2>Download CPI sheet for batch & department</h2>
        <p>Download an Excel sheet for a department batch with CPI, roll number, and name.</p>
        <input type="text" placeholder="Enter Batch Year (e.g., 2021)" value={batchYear} onChange={(e) => setBatchYear(e.target.value)} />
        <select value={program} onChange={(e) => setProgram(e.target.value)}>
          <option value="">Select Program</option>
          {programs.map((prog, index) => <option key={index} value={prog}>{prog}</option>)}
        </select>
        <input type="text" placeholder="Enter Department (e.g., CSE)" value={department} onChange={(e) => setDepartment(e.target.value)} />
        <button className="download-button" onClick={handleBatchDepartmentCpiDownload}>Download Excel</button>
      </div>

      {/* Batch & Department SPI & CPI Download */}
      <div className="card">
        <h2>Download SPI & CPI sheet for batch & department</h2>
        <p>Download an Excel sheet for a department batch with SPI for each semester, CPI (till that semester), roll number, and name.</p>
        <input type="text" placeholder="Enter Batch Year (e.g., 2021)" value={batchYear} onChange={(e) => setBatchYear(e.target.value)} />
        <select value={program} onChange={(e) => setProgram(e.target.value)}>
          <option value="">Select Program</option>
          {programs.map((prog, index) => <option key={index} value={prog}>{prog}</option>)}
        </select>
        <input type="text" placeholder="Enter Department (e.g., CSE)" value={department} onChange={(e) => setDepartment(e.target.value)} />
        <button className="download-button" onClick={handleBatchDepartmentSpiCpiDownload}>Download Excel</button>
      </div>

      {/* Course-wide Grade Report */}
      <div className="card">
        <h2>Search course and download all grades</h2>
        <p>Download all student grades for a specific course, with names and roll numbers.</p>
        <input type="text" placeholder="Enter Course Code" value={courseCode} onChange={(e) => setCourseCode(e.target.value)} />
        <input type="text" placeholder="Enter Semester Name" value={semesterName} onChange={(e) => setSemesterName(e.target.value)} />
        <input type="text" placeholder="Enter Academic Year" value={academicYear} onChange={(e) => setAcademicYear(e.target.value)} />
        <button className="download-button" onClick={handleCourseGradesDownload}>Download Grades</button>
      </div>

      {/* Calculate Average, High, Low */}
      <div className="card">
        <h2>Calculate Average, High, Low (CPI or SPI)</h2>
        <p>Calculate statistics for CPI or SPI, by batch, department, course, or semester.</p>
        <select value={metric} onChange={(e) => setMetric(e.target.value)}>
          <option value="cpi">CPI</option>
          <option value="spi">SPI</option>
        </select>
        <input type="text" placeholder="Enter Batch Year (e.g., 2021)" value={batchYear} onChange={(e) => setBatchYear(e.target.value)} />
        <select value={program} onChange={(e) => setProgram(e.target.value)}>
          <option value="">Select Program</option>
          {programs.map((prog, index) => <option key={index} value={prog}>{prog}</option>)}
        </select>
        <input type="text" placeholder="Department (optional)" value={department} onChange={(e) => setDepartment(e.target.value)} />
        <input type="text" placeholder="Semester (optional)" value={semesterName} onChange={(e) => setSemesterName(e.target.value)} />
        <input type="text" placeholder="Course Code (optional)" value={courseCode} onChange={(e) => setCourseCode(e.target.value)} />
        <button className="calculate-button" onClick={handleStatisticsCalculation}>Calculate</button>
      </div>

      {/* Grade Distribution Analysis */}
<div className="card">
  <h2>Grade Distribution Analysis</h2>
  <p>View the distribution of grades like AA, AB, etc., for a semester, either whole or course-wise.</p>
  <input type="text" placeholder="Enter Semester Name" value={semesterName} onChange={(e) => setSemesterName(e.target.value)} />
  <input type="text" placeholder="Enter Academic Year" value={academicYear} onChange={(e) => setAcademicYear(e.target.value)} />
  <input type="text" placeholder="Enter Batch Year (e.g., 2021)" value={batchYear} onChange={(e) => setBatchYear(e.target.value)} />
  <select value={program} onChange={(e) => setProgram(e.target.value)}>
    <option value="">Select Program</option>
    {programs.map((prog, index) => <option key={index} value={prog}>{prog}</option>)}
  </select>
  <input type="text" placeholder="Enter Department (optional)" value={department} onChange={(e) => setDepartment(e.target.value)} />
  <select value={gradeView} onChange={(e) => setGradeView(e.target.value)}>
    <option value="whole">Whole</option>
    <option value="course-wise">Course-Wise</option>
  </select>
  <button className="view-chart-button" onClick={handleGradeDistributionFetch}>View Chart</button>
  {Object.keys(grades).length > 0 && <BarChart grades={grades} />}
</div>


      {/* Custom Query */}
      <div className="card">
        <h2>Custom Query</h2>
        <p>Enter a custom query using the available tables.</p>
                  <p><strong>SPI_CPI:</strong> Stores SPI and CPI data with <code>student_id</code>, <code>semester_id</code>, <code>spi</code>, and <code>cpi</code>.</p>
          <p><strong>Grades:</strong> Stores course grades with <code>student_id</code>, <code>course_id</code>, <code>semester_id</code>, and <code>numeric_grade or special_grade_id</code>.</p>
          <p><strong>Courses:</strong> Contains course details with <code>course_code</code>, <code>course_name</code>, and <code>department_id</code>.</p>
          <p><strong>Semesters:</strong> Defines semesters with <code>semester_name_id</code>, <code>academic_year_id</code>, <code>start_month</code>, and <code>end_month</code>.</p>
        <input type="text" placeholder="Enter Custom Query" value={customQuery} onChange={(e) => setCustomQuery(e.target.value)} />
        <button className="search-button" onClick={handleCustomQueryDownload}>Search and Download CSV</button>
      </div>
    </div>
  );
};

export default SearchGrades;


