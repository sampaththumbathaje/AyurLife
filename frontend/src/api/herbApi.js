/**
 * herbApi.js
 * ----------
 * Herb Knowledge Base API service for AyurLife frontend.
 */

import api from "./axiosConfig";

// -----------------------------
// Get All Herbs
// -----------------------------
export const getAllHerbs = async () => {
  const response = await api.get("/herb/herbs");
  return response.data;
};

// -----------------------------
// Get Herb by INTERNAL ID (H001)
// -----------------------------
export const getHerbById = async (herbId) => {
  const response = await api.get(`/herb/herbs/id/${herbId}`);
  return response.data;
};

// -----------------------------
// Get Herb by NAME (Tulsi)
// -----------------------------
export const getHerbByName = async (name) => {
  const response = await api.get(`/herb/herbs/name/${name}`);
  return response.data;
};

// -----------------------------
// Search Herbs
// -----------------------------
export const searchHerbs = async ({
  query = "",
  use = "",
  dosha = "",
} = {}) => {
  const params = {};

  if (query) params.q = query;
  if (use) params.use = use;
  if (dosha) params.dosha = dosha;

  const response = await api.get("/herb/herbs/search", { params });
  return response.data;
};
