/**
 * remedyApi.js
 * ------------
 * Remedy API service for AyurLife frontend.
 */

import api from "./axiosConfig";

// --------------------------------------------------
// Get Remedy Details by Name
// --------------------------------------------------
export const getRemedyByName = async (remedyName) => {
  const response = await api.get(
    `/remedy/${encodeURIComponent(remedyName)}`
  );
  return response.data;
};


// --------------------------------------------------
// Save Remedy to User Dashboard
// --------------------------------------------------
export const saveRemedy = async ({ userId, name }) => {
  const payload = {
    user_id: userId,
    name,
  };

  const response = await api.post(
    `/remedy/save`,
    payload
  );

  return response.data;
};


// --------------------------------------------------
// Get Saved Remedies for User
// --------------------------------------------------
export const getSavedRemedies = async (userId) => {
  const response = await api.get(
    `/remedy/saved/${userId}`
  );

  return response.data;
};


// --------------------------------------------------
// Get Remedies by Prakriti
// --------------------------------------------------
export const getRemediesByPrakriti = async (prakritiType) => {
  const response = await api.get(
    `/remedy/prakriti/${prakritiType}`
  );

  return response.data;
};
