/**
 * config.js
 * ---------
 * Centralized frontend configuration.
 */

const config = {
  // API Configuration
  API_BASE_URL:
    process.env.REACT_APP_API_BASE_URL ||
    "http://localhost:5000/api",

  // App Info
  APP_NAME: "AyurLife",
  APP_VERSION: "1.0.0",

  // Feature Flags
  FEATURES: {
    CHATBOT: true,
    PRAKRITI: true,
    DINACHARYA: true,
    HERB_KNOWLEDGE_BASE: true,
  },

  // Chatbot Settings
  CHATBOT: {
    TYPING_DELAY_MS: 600,
    MAX_MESSAGE_LENGTH: 500,
  },

  // Pagination Defaults
  PAGINATION: {
    PAGE_SIZE: 10,
  },
};

export default config;
