import React from 'react';
import './AdminDashboard.css';
import Card from '../Card/Card';

const AdminDashboard = () => {
  const adminActions = [
    {
      title: 'Set Grading System Configurations',
      description: 'Configure the grading rules and policies for each academic year and batch.',
      buttonText: 'Go to Grading Config',
      onButtonClick: () => window.location.href = '/admin/grading-config',
    },
    {
      title: 'Set PDF Description',
      description: 'Manage the content that appears at the bottom of each student’s grade report.',
      buttonText: 'Go to PDF Description',
      onButtonClick: () => window.location.href = '/admin/pdf-description',
    },
    {
      title: 'View Audited Logs',
      description: 'Check system logs for important actions, changes, and events.',
      buttonText: 'Go to Logs',
      onButtonClick: () => window.location.href = '/admin/logs',
    },
  ];

  return (
    <div className="admin-dashboard">
      <h1>Admin Dashboard</h1>
      <div className="cards-container">
        {adminActions.map((action, index) => (
          <Card
            key={index}
            title={action.title}
            description={action.description}
            buttonText={action.buttonText}
            onButtonClick={action.onButtonClick}
          />
        ))}
      </div>
    </div>
  );
};

export default AdminDashboard;
