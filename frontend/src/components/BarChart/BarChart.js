import React from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Tooltip, Legend } from 'chart.js';
import './BarChart.css'
// Register the required components
ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

const BarChart = ({ grades }) => {
  const data = {
    labels: Object.keys(grades),
    datasets: [
      {
        label: 'Number of Students',
        data: Object.values(grades),
        backgroundColor: 'rgba(234, 222, 235, 0.6)', // Darker color for bars
        borderColor: 'rgba(54, 42, 35, 1)',
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      x: {
        title: {
          display: true,
          text: 'Grades',
        },
      },
      y: {
        title: {
          display: true,
          text: 'Number of Students',
        },
        beginAtZero: true,
      },
    },
    plugins: {
      legend: {
        display: false,
      },
    },
  };

  return (
    <div className="bar-chart-container">
      <Bar data={data} options={options} />
    </div>
  );
};

export default BarChart;
