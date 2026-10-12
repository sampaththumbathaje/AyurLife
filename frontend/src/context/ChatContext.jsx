import React, {
  createContext,
  useContext,
  useState,
  useCallback,
} from "react";

import { sendChatMessage } from "../api/chatbotApi";
import { useAuth } from "./AuthContext";

/**
 * ChatContext
 * -----------
 * Global chatbot state & actions.
 */
export const ChatContext = createContext(null);


// -----------------------------
// Provider
// -----------------------------
export const ChatProvider = ({ children }) => {
  const { user } = useAuth();

  const [messages, setMessages] = useState([]);
  const [sessionId, setSessionId] = useState(null);
  const [loading, setLoading] = useState(false);

  // -----------------------------
  // Add Message (local helper)
  // -----------------------------
  const addMessage = useCallback((msg) => {
    setMessages((prev) => [...prev, msg]);
  }, []);

  // -----------------------------
  // Reset Chat
  // -----------------------------
  const resetChat = () => {
    setMessages([]);
    setSessionId(null);
  };

  // -----------------------------
  // Send User Message
  // -----------------------------
  const sendMessage = async (text) => {
    if (!user || !text?.trim()) return;

    // Add user message immediately
    addMessage({
      sender: "user",
      text,
    });

    setLoading(true);

    try {
      const response = await sendChatMessage({
        userId: user.id,
        message: text,
        sessionId,
      });

      // Initialize session
      if (response.session_id && !sessionId) {
        setSessionId(response.session_id);
      }

      // Add bot message
      addMessage({
        sender: "bot",
        text: response.message || response.reply,
        data: response,
        questions: response.questions || null,
      });
    } catch (err) {
      addMessage({
        sender: "bot",
        text:
          "Sorry, something went wrong. Please try again.",
      });
    } finally {
      setLoading(false);
    }
  };

  // -----------------------------
  // Submit Prakriti Answers
  // -----------------------------
  const submitPrakritiAnswers = async (answers) => {
    if (!user || !answers) return;

    setLoading(true);

    try {
      const response = await sendChatMessage({
        userId: user.id,
        message: "prakriti answers",
        sessionId,
        prakritiAnswers: answers,
      });

      addMessage({
        sender: "bot",
        text: response.message,
        data: response,
      });
    } catch (err) {
      addMessage({
        sender: "bot",
        text:
          "Failed to submit answers. Please try again.",
      });
    } finally {
      setLoading(false);
    }
  };

  const value = {
    messages,
    sessionId,
    loading,
    sendMessage,
    submitPrakritiAnswers,
    resetChat,
  };

  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  );
};

// -----------------------------
// Hook
// -----------------------------
export const useChat = () => {
  const context = useContext(ChatContext);

  if (!context) {
    throw new Error(
      "useChat must be used within a ChatProvider"
    );
  }

  return context;
};
