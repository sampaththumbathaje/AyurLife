import React, { useEffect, useState } from "react";
import Sidebar from "../common/Sidebar";
import Loader from "../common/Loader";

import {
  assignPlannerTask,
  getUserPlanner,
  completePlannerTask,
  deletePlannerTask,
} from "../../api/plannerApi";

import { getCurrentUser } from "../../api/authApi";
import TaskItem from "./TaskItem";

// ✅ LOCAL TASKS
import defaultDinacharyaTasks from "../../data/dinacharyaTasks";

const Dinacharya = () => {

  const [user, setUser] = useState(null);

  const [availableTasks, setAvailableTasks] = useState([]);
  const [userTasks, setUserTasks] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // ✅ Custom Task States
  const [customTaskName, setCustomTaskName] =
    useState("");

  const [customTaskTime, setCustomTaskTime] =
    useState("06:00");

  const today =
    new Date().toISOString().split("T")[0];

  // =====================================================
  // LOAD USER
  // =====================================================

  useEffect(() => {

    const u = getCurrentUser();

    setUser(u);

  }, []);

  // =====================================================
  // LOAD DATA
  // =====================================================

  useEffect(() => {

    if (!user) return;

    const fetchData = async () => {

      try {

        setLoading(true);

        // ✅ LOCAL AYURVEDIC TASKS
        setAvailableTasks(
          defaultDinacharyaTasks
        );

        const planner =
          await getUserPlanner(user.id);

        setUserTasks(
          planner.tasks || planner
        );

      } catch (err) {

        setError(
          err.response?.data?.error ||
          "Failed to load planner"
        );

      } finally {

        setLoading(false);

      }
    };

    fetchData();

  }, [user]);

  // =====================================================
  // ASSIGN TASK
  // =====================================================

  const handleAssignTask = async (task) => {

    try {

      await assignPlannerTask({
        userId: user.id,
        taskId: task.task_id,
        taskName: task.task_name,
        time: task.time || "06:00",
        date: today,
      });

      const planner =
        await getUserPlanner(user.id);

      setUserTasks(
        planner.tasks || planner
      );

    } catch {

      alert("Failed to assign task");

    }
  };

  // =====================================================
  // ADD CUSTOM TASK
  // =====================================================

  const handleAddCustomTask = async () => {

    if (!customTaskName.trim()) {

      alert("Please enter a task name");

      return;
    }

    try {

      await assignPlannerTask({
        userId: user.id,
        taskId: `custom-${Date.now()}`,
        taskName: customTaskName,
        time: customTaskTime,
        date: today,
      });

      const planner =
        await getUserPlanner(user.id);

      setUserTasks(
        planner.tasks || planner
      );

      // RESET
      setCustomTaskName("");
      setCustomTaskTime("06:00");

    } catch {

      alert("Failed to add custom task");

    }
  };

  // =====================================================
  // COMPLETE TASK
  // =====================================================

  const handleCompleteTask = async (task) => {

    try {

      const taskId =
        task.task_id ||
        task.id ||
        task._id;

      await completePlannerTask({
        userId: user.id,
        taskId,
        date: task.date,
      });

      // ✅ INSTANT UI UPDATE
      setUserTasks((prevTasks) =>
        prevTasks.map((t) => {

          const currentId =
            t.task_id ||
            t.id ||
            t._id;

          if (
            currentId === taskId &&
            t.date === task.date
          ) {
            return {
              ...t,
              completed: true,
            };
          }

          return t;
        })
      );

      // ✅ BACKEND SYNC
      const planner =
        await getUserPlanner(user.id);

      setUserTasks(
        planner.tasks || planner
      );

    } catch (err) {

      console.error(
        "Complete Task Error:",
        err
      );

      alert("Failed to update task");
    }
  };

  // =====================================================
  // DELETE TASK
  // =====================================================

  const handleDeleteTask = async (task) => {

    try {

      await deletePlannerTask({
        userId: user.id,
        taskId: task.task_id,
        date: task.date,
      });

      // ✅ REMOVE FROM UI
      setUserTasks((prevTasks) =>
        prevTasks.filter((t) => {

          return !(
            t.task_id === task.task_id &&
            t.date === task.date
          );
        })
      );

      // ✅ BACKEND SYNC
      const planner =
        await getUserPlanner(user.id);

      setUserTasks(
        planner.tasks || planner
      );

    } catch (err) {

      console.error(
        "Delete Task Error:",
        err
      );

      alert("Failed to delete task");
    }
  };

  // =====================================================
  // LOADING / ERROR
  // =====================================================

  if (!user)
    return (
      <Loader message="Authenticating..." />
    );

  if (loading)
    return (
      <Loader message="Loading Dinacharya..." />
    );

  if (error)
    return (
      <div className="planner-error">
        {error}
      </div>
    );

  // =====================================================
  // UI
  // =====================================================

  return (
    <div className="planner-container">

      <Sidebar />

      <main className="planner-main">

        {/* HEADER */}
        <div className="planner-header">

          <div>
            <h1>Dinacharya Planner</h1>

            <p className="planner-subtitle">
              Build healthy Ayurvedic habits
              for a balanced life
            </p>
          </div>

          <div className="quote-card">

            <p className="quote-text">
              “When diet is wrong,
              medicine is of no use.”
            </p>

            <span>
              — Ayurvedic Proverb
            </span>

          </div>
        </div>

        {/* TODAY TASKS */}
        <section className="planner-card">

          <h3>Today's Dinacharya</h3>

          {userTasks.filter(
            (t) => t.date === today
          ).length === 0 ? (

            <p className="muted-text">
              No tasks scheduled for today.
            </p>

          ) : (

            userTasks
              .filter(
                (t) => t.date === today
              )
              .map((task, index) => (

                <TaskItem
                  key={index}
                  task={task}
                  onComplete={
                    handleCompleteTask
                  }
                  onDelete={
                    handleDeleteTask
                  }
                />

              ))
          )}
        </section>

        {/* CUSTOM TASK */}
        <section className="planner-card">

          <h3>Add Custom Task</h3>

          <div className="custom-task-form">

            <input
              type="text"
              placeholder="Enter task name..."
              value={customTaskName}
              onChange={(e) =>
                setCustomTaskName(
                  e.target.value
                )
              }
            />

            <input
              type="time"
              value={customTaskTime}
              onChange={(e) =>
                setCustomTaskTime(
                  e.target.value
                )
              }
            />

            <button
              className="add-task-btn"
              onClick={
                handleAddCustomTask
              }
            >
              + Add Task
            </button>

          </div>
        </section>

        {/* AVAILABLE TASKS */}
        <section className="planner-card">

          <h3>
            Available Dinacharya Practices
          </h3>

          <div className="available-task-grid">

            {availableTasks.map(
              (task, index) => (

                <div
                  key={index}
                  className="available-task"
                >

                  <h4>
                    {task.task_name}
                  </h4>

                  <p>
                    {task.description}
                  </p>

                  <small
                    style={{
                      color: "#0f8b4c",
                      fontWeight: "600",
                    }}
                  >
                    ⏰ {task.time}
                  </small>

                  <button
                    className="add-task-btn"
                    onClick={() =>
                      handleAssignTask(task)
                    }
                  >
                    + Add to Today
                  </button>

                </div>
              )
            )}
          </div>
        </section>

      </main>
    </div>
  );
};

export default Dinacharya;