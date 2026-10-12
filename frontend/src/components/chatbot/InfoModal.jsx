import React from "react";

const InfoModal = ({
  isOpen,
  onClose,
  title,
  content,
}) => {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="info-modal">

        {/* Header */}
        <div className="info-modal-header">
          <h3>{title}</h3>

          <button
            className="modal-close-btn"
            onClick={onClose}
          >
            ✕
          </button>
        </div>

        {/* Content */}
        <div className="info-modal-content">
          <p>{content}</p>
        </div>

        {/* Footer */}
        <div className="info-modal-footer">
          <button
            className="modal-ok-btn"
            onClick={onClose}
          >
            Got it
          </button>
        </div>

      </div>
    </div>
  );
};

export default InfoModal;