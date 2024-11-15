import React, { useState, useEffect } from 'react';
import './Login.css';
import axios from 'axios';
import { useNavigate, useLocation } from 'react-router-dom';
import Alert from '../Alert/Alert'; // Adjust the path accordingly

const Login = ({ setIsLoggedIn, setUserType, setUserName, setUserEmail }) => {
  const [isStudent, setIsStudent] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showAlert, setShowAlert] = useState(false);
  const [alertMessage, setAlertMessage] = useState('');

  const navigate = useNavigate(); // Hook to handle navigation
  const location = useLocation(); // Hook to access location state

  // Check if there's an alert message in the navigation state
  useEffect(() => {
    if (location.state && location.state.alertMessage) {
      setAlertMessage(location.state.alertMessage);
      setShowAlert(true);
    }
  }, [location.state]);

  const handleToggle = (userType) => {
    setIsStudent(userType === 'student');
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    const userType = isStudent ? 'student' : 'staff';

    try {
      const response = await axios.post('/login', {
        email,
        password,
        user_type: userType,
      });

      if (response.data.token) {
        localStorage.setItem('token', response.data.token);
        localStorage.setItem(
          'userData',
          JSON.stringify({
            userType: response.data.userRole,
            userName: response.data.userName,
            email: email
          })
        );

        // Set login state in App.js
        setIsLoggedIn(true);
        setUserType(response.data.userRole);
        setUserName(response.data.userName);  // Set username
        setUserEmail(email);

        // Redirect based on user role directly
        navigate(`/${response.data.userRole}`);
      }
    } catch (error) {
      setAlertMessage('Login failed. Please check your credentials.');
      setShowAlert(true);
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        {showAlert && <Alert message={alertMessage} onClose={() => setShowAlert(false)} />}
        <div className="toggle-switch">
          <button
            className={`toggle-btn ${isStudent ? 'active' : ''}`}
            onClick={() => handleToggle('student')}
          >
            Student Portal
          </button>
          <button
            className={`toggle-btn ${!isStudent ? 'active' : ''}`}
            onClick={() => handleToggle('staff')}
          >
            Staff Portal
          </button>
        </div>
        <h1>{isStudent ? 'STUDENT LOGIN' : 'STAFF LOGIN'}</h1>
        <form onSubmit={handleLogin}>
          <input
            type="email"
            placeholder="Email id"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button type="submit">Login</button>
        </form>
      </div>
    </div>
  );
};

export default Login;
