import React from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { logoutUser, getCurrentUser } from "../../api/authApi";

const Sidebar = () => {
  const navigate = useNavigate();
  const user = getCurrentUser();

  const handleLogout = () => {
    logoutUser();
    navigate("/", { replace: true }); // ✅ go to Home
  };

  if (!user) return null;

  return (
    <aside className="app-sidebar">
      {/* User Section */}
      <div className="sidebar-header">
        <div className="sidebar-avatar">
          {user.name?.charAt(0).toUpperCase()}
        </div>

        <div>
          <p className="sidebar-username">{user.name}</p>
          <p className="sidebar-email">{user.email}</p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="sidebar-nav">
        <NavLink to="/dashboard" className="sidebar-link">
          Dashboard
        </NavLink>

        <NavLink to="/chatbot" className="sidebar-link">
          Chatbot
        </NavLink>

        <NavLink to="/planner" className="sidebar-link">
          Dinacharya
        </NavLink>

        <NavLink to="/herbs" className="sidebar-link">
          Herb Knowledge
        </NavLink>
      </nav>

      {/* Footer */}
      <div className="sidebar-footer">
        <button
          className="sidebar-logout"
          onClick={handleLogout}
        >
          Logout
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
