/**
 * authApi.js
 * ----------
 *
 * Authentication API service for AyurLife frontend.
 * Uses centralized Axios instance.
 * Uses sessionStorage for auto-logout on app close.
 */

import api from "./axiosConfig";

// -----------------------------
// Register User
// -----------------------------
export const registerUser = async (payload) => {
  const response = await api.post("/auth/register", payload);
  return response.data;
};

// -----------------------------
// Login User
// -----------------------------
export const loginUser = async (payload) => {
  const response = await api.post("/auth/login", payload);

  // ✅ Store token & user in sessionStorage (auto logout on close)
  if (response.data.token) {
    sessionStorage.setItem("auth_token", response.data.token);
    sessionStorage.setItem(
      "user",
      JSON.stringify(response.data.user)
    );
  }

  return response.data;
};

// -----------------------------
// Logout User
// -----------------------------
export const logoutUser = () => {
  sessionStorage.removeItem("auth_token");
  sessionStorage.removeItem("user");
};

// -----------------------------
// Get Logged-in User
// -----------------------------
export const getCurrentUser = () => {
  const user = sessionStorage.getItem("user");
  return user ? JSON.parse(user) : null;
};
