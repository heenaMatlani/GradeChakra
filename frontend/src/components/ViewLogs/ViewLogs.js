import React, { useState, useEffect } from 'react';
import axios from 'axios';  // Import Axios
import './ViewLogs.css';

const ViewLogs = () => {
  const [logs, setLogs] = useState([]);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [startTime, setStartTime] = useState('');
  const [endTime, setEndTime] = useState('');
  const [actionFilter, setActionFilter] = useState('');
  const [filteredLogs, setFilteredLogs] = useState([]);
  const [showFilter, setShowFilter] = useState(false);

  useEffect(() => {
    // Fetch all logs from the backend using Axios
    const fetchLogs = async () => {
      try {
        const response = await axios.get('/logs'); // Use Axios for the GET request
        const data = response.data;

        // Sort logs by latest date and time
        const sortedLogs = data.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
        setLogs(sortedLogs); // Set fetched logs
        setFilteredLogs(sortedLogs); // Show all logs initially
      } catch (error) {
        console.error('Error fetching logs:', error);
      }
    };

    fetchLogs();
  }, []);

  const handleFilter = () => {
    let filtered = logs;

    if (startDate && endDate) {
      filtered = filtered.filter(log => {
        const logDate = new Date(log.timestamp);
        const start = new Date(`${startDate}T${startTime || '00:00'}`);
        const end = new Date(`${endDate}T${endTime || '23:59'}`);
        return logDate >= start && logDate <= end;
      });
    }

    if (actionFilter) {
      filtered = filtered.filter(log => log.action_type === actionFilter);
    }

    setFilteredLogs(filtered);
  };

  const toggleFilter = () => {
    setShowFilter(!showFilter);
  };

  return (
    <div className="logs-container">
      <h2>Logs</h2>

      <div className="top-bar">
        <button onClick={toggleFilter} className="filter-toggle-button">
          {showFilter ? 'Hide Filter' : 'Show Filter'}
        </button>
      </div>

      {showFilter && (
        <div className="filter-container">
          {/* Start Date and Time */}
          <div className="filter-row">
            <div className="filter-row-date">
              <label>Start Date:</label>
              <input
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
              />
            </div>
            <div className="filter-row-time">
              <label>Start Time:</label>
              <input
                type="time"
                value={startTime}
                onChange={(e) => setStartTime(e.target.value)}
              />
            </div>
          </div>

          {/* End Date and Time */}
          <div className="filter-row">
            <div className="filter-row-date">
              <label>End Date:</label>
              <input
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
              />
            </div>
            <div className="filter-row-time">
              <label>End Time:</label>
              <input
                type="time"
                value={endTime}
                onChange={(e) => setEndTime(e.target.value)}
              />
            </div>
          </div>

          {/* Action Filter */}
          <div className="filter-action-row">
            <label>Filter by Action:</label>
            <select value={actionFilter} onChange={(e) => setActionFilter(e.target.value)}>
              <option value="">Select Action</option>
              <option value="Set Grading System">Set Grading System</option>
              <option value="Uploaded Grades">Uploaded Grades</option>
              <option value="Set PDF Description">Set PDF Description</option>
              {/* Add more action types as needed */}
            </select>
          </div>

          {/* Apply Filter Button */}
          <div className="filter-button-row">
            <button onClick={handleFilter}>Apply Filter</button>
          </div>
        </div>
      )}

      <div className="logs-list">
        {filteredLogs.length > 0 ? (
          <table className="logs-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Action Performed</th>
                <th>Employee</th>
                <th>Comments</th> {/* Added Comments Column */}
                <th>Date</th>
                <th>Time</th>
              </tr>
            </thead>
            <tbody>
              {filteredLogs.map((log, index) => (
                <tr key={log.log_id}>
                  <td>{index + 1}</td>
                  <td>{log.action_type}</td>
                  <td>{log.employee_name}</td>
                  <td>{log.comment}</td> {/* Displaying comments here */}
                  <td>{new Date(log.timestamp).toLocaleDateString()}</td>
                  <td>{new Date(log.timestamp).toLocaleTimeString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No logs found.</p>
        )}
      </div>
    </div>
  );
};

export default ViewLogs;
