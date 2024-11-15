import React, { useState, useEffect } from 'react';
import './Profile.css';
import axios from 'axios';

const Profile = ({ userType, userEmail }) => {
  const [userDetails, setUserDetails] = useState(null);
  const [isChangingPassword, setIsChangingPassword] = useState(false);
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  useEffect(() => {
    const fetchProfileData = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('/profile', {
          headers: {
            Authorization: `Bearer ${token}`
          },
          params: {
            user_type: userType,
            email: userEmail
          }
        });

        setUserDetails(response.data);
      } catch (error) {
        console.error('Error fetching profile data:', error);
        alert('Failed to load profile data');
      }
    };

    fetchProfileData();
  }, [userType, userEmail]);

  const handlePasswordChange = async () => {
    if (newPassword !== confirmPassword) {
      alert('New password and confirm password do not match');
      return;
    }

    try {
      const token = localStorage.getItem('token');
      await axios.post('/change-password', {
        oldPassword,
        newPassword,
        userType,
        userEmail
      }, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      alert('Password changed successfully');
      setIsChangingPassword(false);
      setOldPassword('');
      setNewPassword('');
      setConfirmPassword('');
    } catch (error) {
      console.error('Error changing password:', error);
      alert('Failed to change password');
    }
  };

  if (!userDetails) {
    return <div>Loading profile...</div>;
  }

  const { name, rollNo, batch, program, department, email, role, startDate } = userDetails;

  return (
    <div className="profile-container">
      <h2 className="profile-header">{userType === 'student' ? 'Student Profile' : 'User Profile'}</h2>
      <div className="profile-details">
        <div className="profile-item">
          <span className="profile-label">Name:</span> {name || 'N/A'}
        </div>
        {userType === 'student' ? (
          <>
            <div className="profile-item">
              <span className="profile-label">Roll No:</span> {rollNo || 'N/A'}
            </div>
            <div className="profile-item">
              <span className="profile-label">Batch:</span> {batch || 'N/A'}
            </div>
            <div className="profile-item">
              <span className="profile-label">Program:</span> {program || 'N/A'}
            </div>
          </>
        ) : (
          <>
            <div className="profile-item">
              <span className="profile-label">Role:</span> {role || 'N/A'}
            </div>
            <div className="profile-item">
              <span className="profile-label">Start Date:</span> {startDate || 'N/A'}
            </div>
          </>
        )}
        <div className="profile-item">
          <span className="profile-label">Department:</span> {department || 'N/A'}
        </div>
        <div className="profile-item">
          <span className="profile-label">Email:</span> {email || 'N/A'}
        </div>
      </div>

      <div className="button-container">
      <button onClick={() => setIsChangingPassword(!isChangingPassword)} className="change-password-button">
        {isChangingPassword ? 'Cancel' : 'Change Password'}
      </button>
          </div>

      {isChangingPassword && (
        <div className="password-change-form">
          <input
            type="password"
            placeholder="Old Password"
            value={oldPassword}
            onChange={(e) => setOldPassword(e.target.value)}
          />
          <input
            type="password"
            placeholder="New Password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
          />
          <input
            type="password"
            placeholder="Confirm New Password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
                <div className="button-container">
          <button onClick={handlePasswordChange} className="submit-password-change">
            Submit
          </button>
              </div>
        </div>
      )}
    </div>
  );
};

export default Profile;
