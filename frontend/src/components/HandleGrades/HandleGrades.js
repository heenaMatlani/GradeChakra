import React, { useState } from 'react';
import './HandleGrades.css'; // Import the CSS file

const HandleGrades = () => {
  const [option, setOption] = useState('uploadExcel'); // Default to upload Excel
   // Initialize JSON for grades
  const [gradesData, setGradesData] = useState([{
    roll_number: '',
    course_code: '',
    grade: '',
    employee_id: '',
    grade_type: '',
    semester: '',
    academic_year: '',
    elective_change: '',
    new_course_code: '',
    previous_course_id: ''
  }]);
  const [excelFile, setExcelFile] = useState(null);

  const handleOptionChange = (e) => {
    setOption(e.target.value);
  };

  const handleGradeChange = (index, field, value) => {
    const newData = [...gradesData];
    newData[index][field] = value;
    setGradesData(newData);
  };

  const addGradeRow = () => {
    setGradesData([...gradesData, {
      roll_number: '',
      course_code: '',
      grade: '',
      employee_id: '',
      grade_type: '',
      semester: '',
      academic_year: '',
      elective_change: '',
      new_course_code: '',
      previous_course_id: ''
    }]);
  };

  const removeGradeRow = (index) => {
    const newData = gradesData.filter((_, i) => i !== index);
    setGradesData(newData);
  };

  const handleExcelUpload = (e) => {
    setExcelFile(e.target.files[0]);
  };


    const [isProcessing, setIsProcessing] = useState(false);
  const [downloadLink, setDownloadLink] = useState(null); // For zip file download link
  const [zipFile, setZipFile] = useState(null);

const handleSubmit = async () => {
    const confirmation = window.confirm("Are you sure you want to submit the grades?");
    if (confirmation) {
          setIsProcessing(true);

      if (option === 'uploadExcel' && excelFile) {
        const formData = new FormData();
        formData.append('excelFile', excelFile);

        // Send the form data (Excel file) to the backend
        try {
        console.log("excel");
          const response = await fetch('/upload-grades', {
            method: 'POST',
            body: formData
          });
          const data = await response.json();
          alert(data.message);

                  } catch (error) {
          console.error("Error uploading grades:", error);
        }
        finally {
          setIsProcessing(false);
        }
      } else if (option === 'fillBoxes') {
        const gradesJson = { grades: gradesData };

        // Send JSON data from fill-out boxes to the backend
        try {
          const response = await fetch('/upload-grades', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(gradesJson)
          });
          const data = await response.json();
          alert(data[0].message);
               }catch (error) {
          console.error("Error uploading grades:", error);
        }
        finally {
          setIsProcessing(false);
        }
      }
    }
  };

  const handleZipUpload = (e) => setZipFile(e.target.files[0]);

  const handleZipSubmit = async () => {
    if (!zipFile) return;

    const formData = new FormData();
    formData.append('zipFile', zipFile);

    try {
      const response = await fetch('/upload-zip', {
        method: 'POST',
        body: formData
      });
      const result = await response.json();

      if (result.message) {
        alert(result.message);
      }
    } catch (error) {
      console.error("Error uploading ZIP file:", error);
      alert("There was an error uploading the ZIP file.");
    }
  };

    const handleAutomaticPDFGeneration = async () => {

    try {
      const response = await fetch('/generate-pdfs', {
        method: 'POST',
        body:  downloadLink
      });
      const result = await response.json();

      if (result.message) {
        alert(result.message);
      }
    } catch (error) {
      console.error("Error generating PDFs:", error);
      alert("There was an error generating PDFs automatically.");
    }
  };

  return (
    <div className="change-upload-grades">
      <h2>Handle Grades</h2>
      <div className="change-upload-toggle-switch">
        <div className={`change-upload-toggle-btn ${option === 'uploadExcel' ? 'active' : ''}`} onClick={() => setOption('uploadExcel')}>
          Upload Excel
        </div>
        <div className={`change-upload-toggle-btn ${option === 'fillBoxes' ? 'active' : ''}`} onClick={() => setOption('fillBoxes')}>
          Fill Out Boxes
        </div>
      </div>

      {/* Conditional rendering for input options */}
      {option === 'uploadExcel' && (
        <div className="option-selector">
          <label htmlFor="excelFile">Upload Excel File:</label>
          <input type="file" id="excelFile" accept=".xlsx, .xls" className="large-input" onChange={handleExcelUpload} />
        </div>
      )}

      {option === 'fillBoxes' && (
        <div className="fill-boxes">
          <h3>Enter Grades:</h3>
          {gradesData.map((grade, index) => (
            <div className="grade-entry" key={index}>
            <div className="remove-add-container">
              <button onClick={() => removeGradeRow(index)} className="remove-grade">Remove below entry</button>
              </div>
              <div className="input-group">
                <label>Roll Number:</label>
                <input
                  type="text"
                  value={grade.roll_number}
                  onChange={(e) => handleGradeChange(index, 'roll_number', e.target.value)}
                  placeholder="2024001"
                />
              </div>
              <div className="input-group">
                <label>Course Code:</label>
                <input
                  type="text"
                  value={grade.course_code}
                  onChange={(e) => handleGradeChange(index, 'course_code', e.target.value)}
                  placeholder="CS102"
                />
              </div>
              <div className="input-group">
                <label>Grade:</label>
                <input
                  type="text"
                  value={grade.grade}
                  onChange={(e) => handleGradeChange(index, 'grade', e.target.value)}
                  placeholder="AA"
                />
              </div>
              <div className="input-group">
                <label>Institute Employee id:</label>
                <input
                  type="text"
                  value={grade.employee_id}
                  onChange={(e) => handleGradeChange(index, 'employee_id', e.target.value)}
                  placeholder="101"
                />
              </div>
              <div className="input-group">
                <label>Grade Type:</label>
                <select
                  value={grade.grade_type}
                  onChange={(e) => handleGradeChange(index, 'grade_type', e.target.value)}
                >
                  <option value="">Select</option>
                  <option value="initial">Initial</option>
                  <option value="repeat">Repeat</option>
                </select>
              </div>
              <div className="input-group">
                <label>Semester:</label>
                <select
                  value={grade.semester}
                  onChange={(e) => handleGradeChange(index, 'semester', e.target.value)}
                >
                  <option value="">Select</option>
                  <option value="Monsoon">Monsoon</option>
                  <option value="Spring">Spring</option>
                </select>
              </div>
              <div className="input-group">
                <label>Academic Year:</label>
                <select
                  value={grade.academic_year}
                  onChange={(e) => handleGradeChange(index, 'academic_year', e.target.value)}
                >
                  <option value="">Select</option>
                  <option value="2023-2024">2023-2024</option>
                  <option value="2024-2025">2024-2025</option>
                </select>
              </div>
              <div className="input-group">
                <label>Elective Change:</label>
                <select
                  value={grade.elective_change}
                  onChange={(e) => handleGradeChange(index, 'elective_change', e.target.value)}
                >
                  <option value="">Select</option>
                  <option value="yes">Yes</option>
                  <option value="no">No</option>
                </select>
              </div>
              {grade.elective_change === 'yes' && (
                <div className="elective-change">
                  <div className="input-group">
                    <label>New Course Code:</label>
                    <input
                      type="text"
                      value={grade.new_course_code}
                      onChange={(e) => handleGradeChange(index, 'new_course_code', e.target.value)}
                      placeholder="CS105"
                    />
                  </div>
                  <div className="input-group">
                    <label>Previous Course ID:</label>
                    <input
                      type="text"
                      value={grade.previous_course_id}
                      onChange={(e) => handleGradeChange(index, 'previous_course_id', e.target.value)}
                      placeholder="CS104"
                    />
                  </div>
                </div>
              )}
            </div>
          ))}
          <div className="remove-add-container">
          <button className="add-grade-row" onClick={addGradeRow}>
            Add Another Grade Entry
          </button>
          </div>
        </div>
      )}

      {/* Submit Button */}
      <div className="button-container">
        <button className="submit-button" onClick={handleSubmit} disabled={isProcessing}>
          {isProcessing ? "Processing..." : "Submit Grades"}
        </button>
      </div>

      {/* Display download options after processing */}
      {/* Display download options after processing */}



    </div>
  );
};

export default HandleGrades;
