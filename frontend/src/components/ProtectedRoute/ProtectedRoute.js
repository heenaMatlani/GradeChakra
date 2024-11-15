import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Alert from '../Alert/Alert'; // Adjust path accordingly

const ProtectedRoute = ({ children, isLoggedIn, userType, requiredUserType }) => {
  const [showAlert, setShowAlert] = useState(false);
  const [isLoading, setIsLoading] = useState(true); // Add loading state
  const navigate = useNavigate(); // Use the `useNavigate` hook for redirection

  console.log(isLoggedIn, userType, requiredUserType);
  useEffect(() => {
    if (!isLoggedIn) {
      setShowAlert(true);

      // Navigate to login page with the alert message
      navigate('/login', { state: { alertMessage: 'Please login to enter that portal.' } });
    } else if (userType !== requiredUserType) {
      setShowAlert(true);

      // Navigate to login page with the alert message
      navigate('/login', { state: { alertMessage: 'Unauthorized access. You do not have permission to view that page. Please login to continue.' } });
    } else {
      setShowAlert(false);
    }
    setIsLoading(false); // Stop loading once checks are done
  }, [navigate]); // Effect depends on these values

  if (isLoading) {
    return <div>Loading...</div>; // Or return a loading spinner
  }

  return children; // If the conditions are met, render the protected content
};

export default ProtectedRoute;
