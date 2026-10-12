import React, {
  createContext,
  useContext,
  useEffect,
  useState,
} from "react";

import {
  loginUser,
  logoutUser,
  getCurrentUser,
} from "../api/authApi";

/**
 * AuthContext
 * -----------
 * Global authentication context.
 * Uses sessionStorage for auto logout on app close.
 */
export const AuthContext = createContext(null);

// -----------------------------
// Auth Provider
// -----------------------------
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // -----------------------------
  // Initialize auth state
  // -----------------------------
  useEffect(() => {
    // ✅ Reads from sessionStorage via authApi
    const storedUser = getCurrentUser();

    if (storedUser) {
      setUser(storedUser);
    } else {
      setUser(null);
    }

    setLoading(false);
  }, []);

  // -----------------------------
  // Login
  // -----------------------------
  const login = async (credentials) => {
    const data = await loginUser(credentials);

    if (data?.user) {
      setUser(data.user);
    }

    return data;
  };

  // -----------------------------
  // Logout
  // -----------------------------
  const logout = () => {
    logoutUser(); // clears sessionStorage
    setUser(null);
  };

  const value = {
    user,
    loading,
    isAuthenticated: !!user,
    login,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// -----------------------------
// Custom Hook
// -----------------------------
export const useAuth = () => {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error(
      "useAuth must be used within an AuthProvider"
    );
  }

  return context;
};
