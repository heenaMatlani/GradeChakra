// Layout.js
import React from 'react';
import Navbar from '../Navbar/Navbar';
import { Outlet } from 'react-router-dom';
import './Layout.css';

const Layout = ({ isLoggedIn, userType, userName }) => {
  return (
    <div className="container">
      <Navbar isLoggedIn={isLoggedIn} userType={userType} />
      <div className="main-content">
        <Outlet /> {/* This is where the child routes will be rendered */}
      </div>
    </div>
  );
};

export default Layout;
