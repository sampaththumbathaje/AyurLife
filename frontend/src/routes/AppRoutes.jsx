import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import useAuth from "../hooks/useAuth";

// Common
import Home from "../components/common/Home";

// Auth
import Login from "../components/auth/Login";
import Register from "../components/auth/Register";

// Protected Pages
import Dashboard from "../components/dashboard/Dashboard";
import Chatbot from "../components/chatbot/Chatbot";
import Dinacharya from "../components/planner/Dinacharya";
import HerbList from "../components/herbs/HerbList";
import HerbDetails from "../components/herbs/HerbDetails";

// =====================================================
// Protected Route Wrapper
// =====================================================

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  // Wait for auth initialization
  if (loading) {
    return <div className="page-loader">Loading...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

// =====================================================
// App Routes
// =====================================================

const AppRoutes = () => {
  const { isAuthenticated, loading } = useAuth();

  // Prevent blank render during auth initialization
  if (loading) {
    return <div className="page-loader">Loading...</div>;
  }

  return (
    <Routes>
      {/* ---------------- Public Routes ---------------- */}

      <Route
        path="/"
        element={
          isAuthenticated ? (
            <Navigate to="/dashboard" replace />
          ) : (
            <Home />
          )
        }
      />

      <Route
        path="/login"
        element={
          isAuthenticated ? (
            <Navigate to="/dashboard" replace />
          ) : (
            <Login />
          )
        }
      />

      <Route
        path="/register"
        element={
          isAuthenticated ? (
            <Navigate to="/dashboard" replace />
          ) : (
            <Register />
          )
        }
      />

      {/* ---------------- Protected Routes ---------------- */}

      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        }
      />

      <Route
        path="/chatbot/:sessionId?"
        element={
          <ProtectedRoute>
            <Chatbot />
          </ProtectedRoute>
        }
      />


      <Route
        path="/planner"
        element={
          <ProtectedRoute>
            <Dinacharya />
          </ProtectedRoute>
        }
      />

      <Route
        path="/herbs"
        element={
          <ProtectedRoute>
            <HerbList />
          </ProtectedRoute>
        }
      />

      <Route
        path="/herbs/:herbId"
        element={
          <ProtectedRoute>
            <HerbDetails />
          </ProtectedRoute>
        }
      />

      {/* ---------------- Fallback ---------------- */}

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};

export default AppRoutes;
