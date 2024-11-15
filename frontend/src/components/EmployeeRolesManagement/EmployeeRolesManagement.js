import React, { useState } from 'react';
import './EmployeeRolesManagement.css';

const EmployeeRoleManagement = () => {
  const [employeeName, setEmployeeName] = useState('');
  const [newRole, setNewRole] = useState('');
  const [fromDate, setFromDate] = useState('');
  const [toDate, setToDate] = useState('');

  const handleSaveRole = () => {
    const confirmation = window.confirm("Are you sure you want to save this role assignment?");
    if (confirmation) {
      // Logic to save the new role assignment (e.g., API call)
      console.log({
        employeeName,
        newRole,
        fromDate,
        toDate,
      });
      // Reset fields after saving
      setEmployeeName('');
      setNewRole('');
      setFromDate('');
      setToDate('');
    }
  };

  return (
    <div className="role-management-container">
      <h2>Employee Role Management</h2>

      <label>Employee Name:</label>
      <select value={employeeName} onChange={(e) => setEmployeeName(e.target.value)}>
        <option value="">Select Employee</option>
        <option value="John Doe">John Doe</option>
        <option value="Jane Smith">Jane Smith</option>
        <option value="Michael Johnson">Michael Johnson</option>
        <option value="Emily Davis">Emily Davis</option>
        {/* Add more employees as needed */}
      </select>

      <label>New Role:</label>
      <select value={newRole} onChange={(e) => setNewRole(e.target.value)}>
        <option value="">Select Role</option>
        <option value="HOD">HOD</option>
        <option value="Dean">Dean</option>
        <option value="Professor">Professor</option>
        <option value="Assistant Professor">Assistant Professor</option>
        {/* Add more roles as needed */}
      </select>

      <label>From Date:</label>
      <input
        type="date"
        value={fromDate}
        onChange={(e) => setFromDate(e.target.value)}
      />

      <label>To Date:</label>
      <input
        type="date"
        value={toDate}
        onChange={(e) => setToDate(e.target.value)}
      />

      <button onClick={handleSaveRole}>Save Role Assignment</button>
    </div>
  );
};

export default EmployeeRoleManagement;
