import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Messages.css';

const Messages = ({ messageType }) => {
  const [messages, setMessages] = useState([]);
  const [filterStatus, setFilterStatus] = useState('all');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  const fetchMessages = async () => {
    try {
      const response = await axios.get(`/messages`, {
        params: {
          type: messageType,
          unreadOnly: filterStatus === 'unread',
          readOnly: filterStatus === 'read',
          startDate,
          endDate,
          page,
          pageSize: 10,
        },
      });
      setMessages(response.data.messages);
      setTotalPages(response.data.totalPages);
    } catch (error) {
      console.error('Error fetching messages:', error);
    }
  };

  useEffect(() => {
    fetchMessages();
  }, [page, messageType]);

  const applyFilters = () => {
    setPage(1); // Reset to first page whenever filters are applied
    fetchMessages();
  };

    useEffect(() => {
    setFilterStatus('all');
    setStartDate('');
    setEndDate('');
    setPage(1);
  }, [messageType]);

  const handleReadChange = async (messageId, isCurrentlyRead) => {
    try {
      const action = isCurrentlyRead ? 'mark-unread' : 'mark-read';
      await axios.put(`/messages/${messageId}/${action}`);
      fetchMessages();
    } catch (error) {
      console.error(`Error marking message as ${isCurrentlyRead ? 'unread' : 'read'}`, error);
    }
  };

  return (
    <div className="messages-container">
      <h2>{messageType === 'student' ? 'Student Issues' : 'Faculty Requests'}</h2>

      <div className="filters">
        <div className="filter-option filter-option-show">
          <select value={filterStatus} onChange={(e) => setFilterStatus(e.target.value)}>
            <option value="all">All</option>
            <option value="unread">Unread</option>
            <option value="read">Read</option>
          </select>
        </div>
        <div className="filter-option">
          <label>Start Date:</label>
          <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
        </div>
        <div className="filter-option">
          <label>End Date:</label>
          <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
        </div>
        <button className="apply-filter" onClick={applyFilters}>Apply Filters</button>
      </div>

      <ul className="messages-list">
        {messages.map((msg) => (
          <li key={msg.request_id} className={`message ${msg.is_read ? 'read' : 'unread'}`}>
            <div className="message-content">
              <p><strong>Name:</strong> {msg.name}</p>
              <p><strong>Email:</strong> {msg.email}</p>
              <p><strong>Message:</strong> {msg.issue_text}</p>
            </div>
        <button
              className="mark-read-btn"
              onClick={() => handleReadChange(msg.request_id, msg.is_read)}
            >                          {msg.is_read ? 'Mark as Unread' : 'Mark as Read'}
            </button>
          </li>
        ))}
      </ul>

      <div className="pagination">
        <button onClick={() => setPage((prev) => Math.max(prev - 1, 1))} disabled={page === 1}>
          Previous
        </button>
        <span>Page {page} of {totalPages}</span>
        <button onClick={() => setPage((prev) => Math.min(prev + 1, totalPages))} disabled={page === totalPages}>
          Next
        </button>
      </div>
    </div>
  );
};

export default Messages;
