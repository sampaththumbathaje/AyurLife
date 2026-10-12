/**
 * plannerApi.js
 * -----------------------------
 *
 * Dinacharya Planner API service for AyurLife frontend.
 */

import api from "./axiosConfig";

// =====================================================
// Get All Dinacharya Tasks
// =====================================================

export const getAllPlannerTasks = async () => {
  const response = await api.get(
    "/planner/tasks"
  );

  return response.data;
};

// =====================================================
// Get Tasks by Prakriti
// =====================================================

export const getPlannerTasksByPrakriti =
  async (prakritiType) => {

    const response = await api.get(
      `/planner/tasks/${prakritiType}`
    );

    return response.data;
  };

// =====================================================
// Assign Task to User Planner
// =====================================================

export const assignPlannerTask =
  async ({
    userId,
    taskId,
    taskName,
    time,
    date,
  }) => {

    const payload = {
      user_id: userId,
      task_id: taskId,
      task_name: taskName,
      time,
      date,
    };

    const response = await api.post(
      "/planner/assign",
      payload
    );

    return response.data;
  };

// =====================================================
// Mark Planner Task as Completed
// =====================================================

export const completePlannerTask =
  async ({
    userId,
    taskId,
    date,
  }) => {

    const payload = {
      user_id: userId,
      task_id: taskId,
      date,
    };

    const response = await api.post(
      "/planner/complete",
      payload
    );

    return response.data;
  };

// =====================================================
// Delete Planner Task
// =====================================================

export const deletePlannerTask =
  async ({
    userId,
    taskId,
    date,
  }) => {

    const payload = {
      user_id: userId,
      task_id: taskId,
      date,
    };

    const response = await api.post(
      "/planner/delete",
      payload
    );

    return response.data;
  };

// =====================================================
// Get User Planner Tasks
// =====================================================

export const getUserPlanner =
  async (userId) => {

    const response = await api.get(
      `/planner/user/${userId}`
    );

    return response.data;
  };