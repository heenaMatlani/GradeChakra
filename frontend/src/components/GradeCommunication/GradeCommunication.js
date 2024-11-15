import React, { useState } from 'react';
import axios from 'axios';
import './GradeCommunication.css';

const GradeCommunication = ({ userType, userEmail }) => {
  const [message, setMessage] = useState('');
  const [statusMessage, setStatusMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!userEmail) {
      setStatusMessage("Session expired. Please log in again.");
      return;
    }

    try {
      const response = await axios.post('/submit-grade-message', {
        userType,
        userEmail,
        message,
      });

      setStatusMessage(response.data.message);
      setMessage('');  // Clear the message box on successful submission
    } catch (error) {
      setStatusMessage(error.response?.data?.error || 'Error submitting message. Please try again.');
      console.error('Error submitting message:', error);
    }
  };

  return (
    <div className="grade-communication">
      <h2>{userType === 'student' ? 'Report an Issue with Grades' : 'Grade Change Request'}</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Describe your message..."
          required
        />
        <button type="submit">Submit</button>
      </form>
      {statusMessage && <p>{statusMessage}</p>}
    </div>
  );
};

export default GradeCommunication;
