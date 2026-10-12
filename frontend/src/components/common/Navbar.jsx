import React from "react";
import { Link, NavLink, useNavigate } from "react-router-dom";
import useAuth from "../../hooks/useAuth";

const Navbar = () => {
  const navigate = useNavigate();

  // ✅ Single source of truth for auth
  const { user, isAuthenticated, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate("/", { replace: true });
  };

  return (
    <nav className="navbar">
      {/* Brand */}
      <div className="navbar-left">
        <Link to="/" className="navbar-brand">
          AyurLife
        </Link>
      </div>

      {/* Navigation */}
      <div className="navbar-right">
        {isAuthenticated ? (
          <>
            <NavLink to="/dashboard" className="nav-link">
              Dashboard
            </NavLink>

            <NavLink to="/chatbot" className="nav-link">
              Chatbot
            </NavLink>

            <NavLink to="/planner" className="nav-link">
              Dinacharya
            </NavLink>

            <NavLink to="/herbs" className="nav-link">
              Herbs
            </NavLink>

            <span className="navbar-user">
              Hi, {user?.name}
            </span>

            <button
              className="nav-btn-outline"
              onClick={handleLogout}
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <NavLink to="/" className="nav-link">
              Home
            </NavLink>

            <NavLink to="/login" className="nav-link">
              Login
            </NavLink>

            <NavLink to="/register" className="nav-btn">
              Register
            </NavLink>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
