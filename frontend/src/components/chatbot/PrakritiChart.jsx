import React from "react";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from "chart.js";
import { Doughnut } from "react-chartjs-2";

ChartJS.register(ArcElement, Tooltip, Legend);

const DOSHA_COLORS = {
  Vata: "#4CAF50",
  Pitta: "#FF9800",
  Kapha: "#2196F3"
};

const PrakritiChart = ({ probabilities, prediction }) => {
  if (!probabilities) return null;

  const labels = Object.keys(probabilities);
  const values = labels.map((key) =>
    Number((probabilities[key] * 100).toFixed(2))
  );

  const backgroundColors = labels.map(
    (label) => DOSHA_COLORS[label] || "#9E9E9E"
  );

  const data = {
    labels,
    datasets: [
      {
        data: values,
        backgroundColor: backgroundColors,
        borderWidth: 1
      }
    ]
  };

  const options = {
    plugins: {
      tooltip: {
        callbacks: {
          label: function (context) {
            return `${context.label}: ${context.raw}%`;
          }
        }
      },
      legend: {
        position: "bottom"
      }
    }
  };

  return (
    <div style={{ width: "320px", margin: "20px auto", textAlign: "center" }}>
      
      {/* Prediction Title */}
      {prediction && (
        <h4 style={{ marginBottom: "10px" }}>
          Dominant: <b>{prediction}</b>
        </h4>
      )}

      <Doughnut data={data} options={options} />

    </div>
  );
};

export default PrakritiChart;
