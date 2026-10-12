import React from "react";
import { Link } from "react-router-dom";
import PrakritiChart from "../chatbot/PrakritiChart";

/**
 * PrakritiCard
 * ------------
 * Displays user's Prakriti information on the dashboard.
 */

const PrakritiCard = ({ prakriti }) => {
  // If no prakriti yet
  if (!prakriti || !prakriti.prediction) {
    return (
      <div className="prakriti-card">
        <h3>Your Prakriti</h3>
        <p className="muted-text">
          Your Prakriti has not been identified yet.
        </p>

        <Link to="/chatbot" className="card-link">
          Identify Prakriti Now →
        </Link>
      </div>
    );
  }

  return (
    <div className="prakriti-card">
      <h3>Your Prakriti</h3>

      {/* Main Prediction */}
      <div className="prakriti-badge">
        🌿 {prakriti.prediction}
      </div>

      {/* Chart */}
      {prakriti.probabilities && (
        <div style={{ marginTop: "15px" }}>
          <PrakritiChart
            probabilities={prakriti.probabilities}
          />
        </div>
      )}

      {/* Date */}
      {prakriti.identified_at && (
        <p className="muted-text">
          Identified on{" "}
          {new Date(
            prakriti.identified_at
          ).toLocaleDateString()}
        </p>
      )}

      <Link to="/planner" className="card-link">
        View Prakriti-based Planner →
      </Link>
    </div>
  );
};

export default PrakritiCard;
