import React, { useState, useEffect, useRef } from 'react';
import './Notifications.css';

const Notifications = ({ notifications }) => {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [notificationList, setNotificationList] = useState(notifications);
  const dropdownRef = useRef(null);

  const toggleDropdown = () => {
    setIsDropdownOpen(!isDropdownOpen);

    // Mark all notifications as read
    setNotificationList(notificationList.map(notification => ({
      ...notification,
      read: true
    })));
  };

  const handleClickOutside = (event) => {
    if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
      setIsDropdownOpen(false); // Close the dropdown if clicked outside
    }
  };

  useEffect(() => {
    if (isDropdownOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    } else {
      document.removeEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isDropdownOpen]);


  return (
    <div className="notification-dropdown" ref={dropdownRef}>
      <span className="notification-icon" onClick={toggleDropdown}>
        {notificationList.some(n => !n.read) ? (
            <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-bell-fill" viewBox="0 0 16 16">
              <path d="M8 16a2 2 0 0 0 2-2H6a2 2 0 0 0 2 2m.995-14.901a1 1 0 1 0-1.99 0A5 5 0 0 0 3 6c0 1.098-.5 6-2 7h14c-1.5-1-2-5.902-2-7 0-2.42-1.72-4.44-4.005-4.901"/>
            </svg>
        ) : (
          <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" className="bi bi-bell" viewBox="0 0 16 16">
            <path d="M8 16a2 2 0 0 0 2-2H6a2 2 0 0 0 2 2M8 1.918l-.797.161A4 4 0 0 0 4 6c0 .628-.134 2.197-.459 3.742-.16.767-.376 1.566-.663 2.258h10.244c-.287-.692-.502-1.49-.663-2.258C12.134 8.197 12 6.628 12 6a4 4 0 0 0-3.203-3.92zM14.22 12c.223.447.481.801.78 1H1c.299-.199.557-.553.78-1C2.68 10.2 3 6.88 3 6c0-2.42 1.72-4.44 4.005-4.901a1 1 0 1 1 1.99 0A5 5 0 0 1 13 6c0 .88.32 4.2 1.22 6"/>
          </svg>
        )}
        {notificationList.some(n => !n.read) && (
          <span className="notification-count">{notificationList.filter(n => !n.read).length}</span>
        )}
      </span>

      {isDropdownOpen && (
        <div className="notification-dropdown-menu">
          <ul>
            {notificationList.slice(0, 10).map((notification, index) => (
              <li key={index} className={notification.read ? 'read' : 'unread'}>
                {notification.message}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};


export default Notifications;
