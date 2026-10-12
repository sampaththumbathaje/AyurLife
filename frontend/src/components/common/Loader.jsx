import React from "react";

/**
 * Loader Component
 * ----------------
 * Reusable loading indicator for async operations.
 *
 * Props:
 * - message (optional): custom loading text
 */
const Loader = ({ message = "Loading..." }) => {
  return (
    <div className="loader-container">
      <div className="loader-spinner" />
      <p className="loader-text">{message}</p>
    </div>
  );
};

export default Loader;
