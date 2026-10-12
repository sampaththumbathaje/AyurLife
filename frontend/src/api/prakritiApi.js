/**
 * prakritiApi.js
 * --------------
 *
 * Prakriti API service for AyurLife frontend.
 * Handles Prakriti questionnaire and prediction.
 */

import api from "./axiosConfig";

// -----------------------------
// Get Prakriti Questionnaire
// -----------------------------
export const getPrakritiQuestions = async () => {
  const response = await api.get("/prakriti/questions");
  return response.data.questions;
};

// -----------------------------
// Submit Prakriti Answers
// -----------------------------
export const submitPrakritiAnswers = async ({ userId, answers }) => {
  const payload = {
    user_id: userId,
    answers,
  };

  const response = await api.post("/prakriti/predict", payload);
  return response.data;
};

// -----------------------------
// Get User Prakriti
// -----------------------------
export const getUserPrakriti = async (userId) => {
  const response = await api.get(`/prakriti/${userId}`);
  return response.data;
};
