import React from 'react';
import './Card.css';

const Card = ({ title, description, buttonText, onButtonClick }) => {
  return (
    <div className="card-container">
      <h3 className="card-title">{title}</h3>
      {description && <p className="card-description">{description}</p>} {/* Display description if it exists */}
      <button className="card-button" onClick={onButtonClick}>
        {buttonText}
      </button>
    </div>
  );
};

export default Card;
