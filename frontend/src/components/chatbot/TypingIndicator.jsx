import React from "react";

/**
 * MessageBubble
 * -------------
 * Renders a single chat message (user or bot).
 *
 * Props:
 * - sender: "user" | "bot"
 * - text: string
 * - options?: string[]        // for Prakriti questions
 * - help?: object             // optional help descriptions
 * - onOptionClick?: function  // callback when option clicked
 */

const MessageBubble = ({
  sender,
  text,
  options,
  help,
  onOptionClick,
}) => {
  const isUser = sender === "user";

  const showHelp = () => {
    if (!help || !help.descriptions) return;

    alert(
      help.descriptions
        .map(
          (d) => `${d.label}:\n${d.text}`
        )
        .join("\n\n")
    );
  };

  return (
    <div
      className={`message-bubble ${
        isUser ? "user-message" : "bot-message"
      }`}
    >
      {/* Message Text */}
      {text && (
        <div className="message-text">
          {text}

          {/* ❗ Help Icon */}
          {help && (
            <span
              className="info-icon"
              onClick={showHelp}
              title="More info"
              style={{ marginLeft: "8px", cursor: "pointer" }}
            >
              ❗
            </span>
          )}
        </div>
      )}

      {/* Prakriti Options */}
      {options && options.length > 0 && (
        <div className="options-container">
          {options.map((opt, idx) => (
            <button
              key={idx}
              className="option-btn"
              onClick={() => onOptionClick(opt)}
            >
              {opt}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default MessageBubble;
