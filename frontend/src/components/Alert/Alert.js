// Alert.js
import React from 'react';
import './Alert.css'; // Import CSS for styling

const Alert = ({ message, onClose }) => {
  return (
    <div className="alert-container">
      <div className="alert-box">
        <span className="alert-message">{message}</span>
        <button className="alert-close" onClick={onClose}>
          &times;
        </button>
      </div>
    </div>
  );
};

export default Alert;
