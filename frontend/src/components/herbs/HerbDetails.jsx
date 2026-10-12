import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

import Sidebar from "../common/Sidebar";
import Loader from "../common/Loader";

import { getHerbByName } from "../../api/herbApi";

const HerbDetails = () => {
  const { herbId } = useParams(); // this is actually the HERB NAME
  const navigate = useNavigate();

  const [herb, setHerb] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // -----------------------------
  // Fetch Herb Details by NAME
  // -----------------------------
  useEffect(() => {
    const fetchHerb = async () => {
      try {
        setLoading(true);
        const data = await getHerbByName(herbId);
        setHerb(data);
      } catch (err) {
        setError(
          err.response?.data?.error ||
            "Failed to load herb details"
        );
      } finally {
        setLoading(false);
      }
    };

    fetchHerb();
  }, [herbId]);

  if (loading) {
    return <Loader message="Loading herb details..." />;
  }

  if (error) {
    return <div>{error}</div>;
  }

  if (!herb) {
    return <div>Herb not found.</div>;
  }

 return (
  <div className="herb-details-container">
    <Sidebar />

    <main className="herb-details-main">
      <button
        className="back-btn"
        onClick={() => navigate("/herbs")}
      >
        ← Back to Herbs
      </button>

      <h1 className="herb-title">{herb.name}</h1>

      {herb.preview && (
        <div className="herb-card full-width">
          <p>{herb.preview}</p>
        </div>
      )}

      <div className="herb-grid">
        {/* Dosha Section */}
        <div className="herb-card">
          <h3>Dosha Effect</h3>

          {herb.pacify && (
            <p>
              <strong>Pacifies:</strong>{" "}
              {herb.pacify.map((d) => (
                <span key={d} className="dosha-badge pacify">
                  {d}
                </span>
              ))}
            </p>
          )}

          {herb.aggravate && (
            <p>
              <strong>Aggravates:</strong>{" "}
              {herb.aggravate.map((d) => (
                <span key={d} className="dosha-badge aggravate">
                  {d}
                </span>
              ))}
            </p>
          )}

          <p>
            <strong>Tridosha:</strong>{" "}
            {herb.tridosha ? "Yes" : "No"}
          </p>
        </div>

        {/* Rasapanchaka Section */}
        <div className="herb-card">
          <h3>Rasapanchaka</h3>

          {herb.rasa && (
            <p>
              <strong>Rasa:</strong>{" "}
              {herb.rasa.join(", ")}
            </p>
          )}

          {herb.guna && (
            <p>
              <strong>Guna:</strong>{" "}
              {herb.guna.join(", ")}
            </p>
          )}

          {herb.virya && (
            <p>
              <strong>Virya:</strong> {herb.virya}
            </p>
          )}

          {herb.vipaka && (
            <p>
              <strong>Vipaka:</strong> {herb.vipaka}
            </p>
          )}
        </div>
      </div>

      {/* Prabhav */}
      {herb.prabhav && (
        <div className="herb-card full-width">
          <h3>Therapeutic Actions (Prabhav)</h3>
          <p>{herb.prabhav.join(", ")}</p>
        </div>
      )}
    </main>
  </div>
);

};

export default HerbDetails;
