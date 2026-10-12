import React from "react";

/**
 * SavedRemedies
 * -------------
 * Displays list of remedies saved by the user.
 */

const SavedRemedies = ({ remedies = [] }) => {
  return (
    <div className="saved-remedies-card">
      <h3>Saved Remedies</h3>

      {remedies.length === 0 ? (
        <p className="muted-text">
          No remedies saved yet.
        </p>
      ) : (
        <ul className="saved-remedy-list">
          {remedies.map((remedy, index) => (
            <li key={index} className="saved-remedy-item">
              <div>
                <strong>{remedy.name}</strong>
                <p className="muted-text">
                  Saved on{" "}
                  {new Date(remedy.saved_at).toLocaleDateString()}
                </p>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default SavedRemedies;
