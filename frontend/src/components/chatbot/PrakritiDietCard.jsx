import React from "react";

const PrakritiDietCard = ({ data }) => {

  if (!data) return null;

  return (
    <div className="prakriti-diet-card">

      <h3>
        {data.dosha} Recommendations
      </h3>

      <div className="diet-section">
        <h4>✅ Diets to Consume</h4>

        <p>{data.consume}</p>
      </div>

      <div className="diet-section">
        <h4>❌ Diets to Avoid</h4>

        <p>{data.avoid}</p>
      </div>

      <div className="diet-section">
        <h4>🌿 Lifestyle</h4>

        <p>{data.lifestyle}</p>
      </div>

    </div>
  );
};

export default PrakritiDietCard;