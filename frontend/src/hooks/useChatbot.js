import { useContext } from "react";
import { ChatContext } from "../context/ChatContext";

/**
 * useChatbot
 * ----------
 * Custom hook to access chatbot context.
 *
 * Returns:
 * - messages
 * - sessionId
 * - loading
 * - sendMessage()
 * - submitPrakritiAnswers()
 * - resetChat()
 */
const useChatbot = () => {
  const context = useContext(ChatContext);

  if (!context) {
    throw new Error(
      "useChatbot must be used within a ChatProvider"
    );
  }

  return context;
};

export default useChatbot;
