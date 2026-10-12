import React, { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";

import Sidebar from "../common/Sidebar";
import Loader from "../common/Loader";

import { getCurrentUser } from "../../api/authApi";
import api from "../../api/axiosConfig";

import PrakritiCard from "./PrakritiCard";

const Dashboard = () => {
  const user = getCurrentUser();

  const [dashboardData, setDashboardData] =
    useState(null);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  // =========================================
  // FETCH DASHBOARD
  // =========================================

  useEffect(() => {
    if (!user?.id) return;

    let isMounted = true;

    const fetchDashboard = async () => {
      try {
        setLoading(true);

        const response = await api.get(
          `/dashboard/${user.id}`
        );

        if (isMounted) {
          setDashboardData(response.data);
        }

      } catch (err) {

        if (isMounted) {
          setError(
            err.response?.data?.error ||
              "Failed to load dashboard"
          );
        }

      } finally {

        if (isMounted) {
          setLoading(false);
        }
      }
    };

    fetchDashboard();

    return () => {
      isMounted = false;
    };

  }, [user?.id]);

  // =========================================
  // AUTH CHECK
  // =========================================

  if (!user) {
    return <Navigate to="/" replace />;
  }

  // =========================================
  // LOADING
  // =========================================

  if (loading) {
    return (
      <Loader message="Loading dashboard..." />
    );
  }

  // =========================================
  // ERROR
  // =========================================

  if (error) {
    return (
      <div className="dashboard-error">
        {error}
      </div>
    );
  }

  if (!dashboardData) return null;

  // =========================================
  // UI
  // =========================================

  return (
    <div className="dashboard-container">

      <Sidebar />

      <main className="dashboard-main">

        {/* =========================================
            HEADER
        ========================================= */}

        <div className="dashboard-header">
          <div>
            <h1>Health Overview</h1>

            <p className="dashboard-subtitle">
              Track your Ayurvedic wellness
              and daily practices
            </p>
          </div>
        </div>

        {/* =========================================
            MAIN GRID
        ========================================= */}

        <div className="dashboard-grid two-column">

          {/* =========================================
              PRAKRITI CARD
          ========================================= */}

          <PrakritiCard
            prakriti={dashboardData.prakriti}
          />

          {/* =========================================
              TODAY TASKS
          ========================================= */}

          <section className="dashboard-card">

            <h3>Today's Dinacharya</h3>

            {dashboardData.today_tasks?.length >
            0 ? (

              <ul className="task-list">

                {dashboardData.today_tasks.map(
                  (task, index) => (

                    <li
                      key={index}
                      className={
                        task.completed
                          ? "done"
                          : ""
                      }
                    >
                      {task.task_name}

                      <span>
                        {task.completed
                          ? "Completed"
                          : "Pending"}
                      </span>
                    </li>
                  )
                )}

              </ul>

            ) : (

              <p className="empty-text">
                No tasks scheduled for today.
              </p>

            )}

          </section>

        </div>

      </main>
    </div>
  );
};

export default Dashboard;