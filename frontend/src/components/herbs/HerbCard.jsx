import React from "react";
import { useNavigate } from "react-router-dom";

const HerbCard = ({ herb }) => {
  const navigate = useNavigate();

  return (
    <div
      className="herb-card"
      onClick={() =>
        navigate(`/herbs/${encodeURIComponent(herb.name)}`)
      }
    >
      <div className="herb-card-header">
        <h4>{herb.name}</h4>
        <span className="heart">♡</span>
      </div>

      <p className="herb-card-preview">
        {herb.preview?.slice(0, 80)}...
      </p>
    </div>
  );
};

export default HerbCard;
