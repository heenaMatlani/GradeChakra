import React, { useState, useRef, useEffect } from 'react';
import './Navbar.css';
import { INSTITUTE_LOGO, INSTITUTE_NAME } from '../../Constants';
import Sidebar from '../Sidebar/Sidebar';
import NotificationDropdown from '../Notifications/Notifications';

const Navbar = ({ isLoggedIn, userType }) => {
  const [showSidebar, setShowSidebar] = useState(false);
  const [showDropdown, setShowDropdown] = useState(false);
  const userDropdownRef = useRef(null); // To refer to the dropdown element

  const dummyNotifications = [
    { message: 'Your grades have been updated.', read: false },
  ];

  const toggleSidebar = () => {
    setShowSidebar(!showSidebar);
  };

  const toggleDropdown = () => {
    setShowDropdown(!showDropdown);
  };

  const handleClickOutside = (event) => {
    if (userDropdownRef.current && !userDropdownRef.current.contains(event.target)) {
      setShowDropdown(false);
    }
  };

  useEffect(() => {
    if (showDropdown) {
      document.addEventListener('mousedown', handleClickOutside);
    } else {
      document.removeEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [showDropdown]);

  const handleLogout = () => {
    localStorage.clear();
    window.location.href = '/login';
  };

  return (
    <>
      <nav className="navbar">
        <div className="navbar-left">
          {isLoggedIn && (
            <div className="hamburger" onClick={toggleSidebar}>
              &#9776;
            </div>
          )}
          <img src={INSTITUTE_LOGO} alt="Institute Logo" className="logo" />
          <span className="institute-name">{INSTITUTE_NAME}</span>
        </div>

        <div className="navbar-right">
          {isLoggedIn ? (
            <>
              {(userType === 'student' || userType === 'faculty') && (
                <NotificationDropdown notifications={dummyNotifications} />
              )}
              <div className="user-dropdown" ref={userDropdownRef}>
                <span className="user-icon" onClick={toggleDropdown}>
                  <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" className="bi bi-person-circle" viewBox="0 0 16 16">
                    <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0"/>
                    <path fillRule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"/>
                  </svg>
                </span>
                <div className={`dropdown-menu ${showDropdown ? 'show' : ''}`}>
                  <ul>
                    <li onClick={() => (window.location.href = `/${userType}/profile`)}>My Profile</li>
                    <li onClick={handleLogout}>Logout</li>
                  </ul>
                </div>
              </div>
            </>
          ) : (
            <span>Welcome to {INSTITUTE_NAME} Grades Portal</span>
          )}
        </div>
      </nav>

      {showSidebar && <Sidebar userType={userType} />}
    </>
  );
};

export default Navbar;
