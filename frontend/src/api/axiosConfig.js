/**
 * axiosConfig.js
 * --------------
 *
 * Central Axios configuration for AyurLife frontend.
 *
 * Responsibilities:
 * - Set API base URL
 * - Attach JWT token automatically
 * - Handle common API errors
 * - Support session-based auto logout
 */

import axios from "axios";

// -----------------------------
// Base Axios Instance
// -----------------------------
const api = axios.create({
  baseURL:
    process.env.REACT_APP_API_BASE_URL ||
    "http://localhost:5000/api",
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 15000, // 15 seconds
});

// -----------------------------
// Request Interceptor
// -----------------------------
api.interceptors.request.use(
  (config) => {
    // ✅ Read token from sessionStorage
    const token = sessionStorage.getItem("auth_token");

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

// -----------------------------
// Response Interceptor
// -----------------------------
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle unauthorized access
    if (error.response && error.response.status === 401) {
      // ✅ Clear session-based auth
      sessionStorage.removeItem("auth_token");
      sessionStorage.removeItem("user");

      // Redirect to login
      window.location.href = "/login";
    }

    return Promise.reject(error);
  }
);

export default api;
