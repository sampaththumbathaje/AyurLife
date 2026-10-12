/**
 * chatbotApi.js
 * -------------
 * Chatbot API service for AyurLife frontend.
 * Handles chat messages, sessions, and Prakriti flow.
 */

import api from "./axiosConfig";

// =====================================================
// SEND CHAT MESSAGE
// =====================================================

export const sendChatMessage = async ({
  userId,
  message,
  sessionId = null,
}) => {
  const payload = {
    user_id: userId,
    message,
    session_id: sessionId,
  };

  const response = await api.post("/chatbot/message", payload);
  return response.data;
};


// =====================================================
// START PRAKRITI FLOW
// =====================================================

export const startPrakritiFlow = async (userId, sessionId = null) => {
  return sendChatMessage({
    userId,
    message: "prakriti",
    sessionId,
  });
};


// =====================================================
// GET FULL CHAT SESSION (NEW)
// =====================================================

export const getChatSession = async (sessionId) => {
  const response = await api.get(`/chatbot/session/${sessionId}`);
  return response.data;
};
