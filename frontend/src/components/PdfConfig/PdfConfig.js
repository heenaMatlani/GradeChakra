import React, { useState } from 'react';
import './PdfConfig.css';

const PDFConfig = () => {
  const [fontStyle, setFontStyle] = useState('Arial');
  const [fontSize, setFontSize] = useState('12');
  const [description, setDescription] = useState('');

  const handleSetConfig = () => {
    const confirmation = window.confirm("Are you sure you want to set this PDF configuration?");
    if (confirmation) {
      // Logic to set PDF configuration
      console.log("PDF configuration set.");
      // Add further actions like API calls here
    }
  };

  const handleDownloadSamplePDF = () => {
    // Logic to download sample PDF (handled by backend)
    console.log("Sample PDF downloaded.");
  };

  return (
    <div className="pdf-config-container">
      <h2>PDF Configuration</h2>

      <label>Font Style:</label>
      <select value={fontStyle} onChange={(e) => setFontStyle(e.target.value)}>
        <option value="Arial">Arial</option>
        <option value="Helvetica">Helvetica</option>
        <option value="Sans-serif">Sans-serif</option>
        <option value="Times New Roman">Times New Roman</option>
        <option value="Courier New">Courier New</option>
      </select>

      <label>Font Size:</label>
      <select value={fontSize} onChange={(e) => setFontSize(e.target.value)}>
        <option value="10">10</option>
        <option value="12">12</option>
        <option value="14">14</option>
        <option value="16">16</option>
        <option value="18">18</option>
      </select>

      <label>Description:</label>
      <textarea
        rows="5"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="Enter description here..."
      />

      <button onClick={handleDownloadSamplePDF}>Download Sample PDF</button>
      <button onClick={handleSetConfig}>Set PDF Configuration</button>
    </div>
  );
};

export default PDFConfig;
