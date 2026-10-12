import React, {
  useState,
  useEffect,
  useRef,
} from "react";

import { useParams } from "react-router-dom";

import {
  sendChatMessage,
  getChatSession,
} from "../../api/chatbotApi";

import { getCurrentUser } from "../../api/authApi";

import MessageBubble from "./MessageBubble";
import TypingIndicator from "./TypingIndicator";
import Loader from "../common/Loader";

const Chatbot = () => {

  const user = getCurrentUser();

  const {
    sessionId: paramSessionId,
  } = useParams();

  const messagesEndRef = useRef(null);

  // =====================================================
  // STATES
  // =====================================================

  const [messages, setMessages] = useState([]);

  const [input, setInput] = useState("");

  const [sessionId, setSessionId] =
    useState(paramSessionId || null);

  const [loading, setLoading] =
    useState(false);

  const [initialLoading, setInitialLoading] =
    useState(false);

  // =====================================================
  // AUTO SCROLL
  // =====================================================

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  // =====================================================
  // LOAD PREVIOUS CHAT SESSION
  // =====================================================

  useEffect(() => {

    const loadSession = async () => {

      if (!paramSessionId) return;

      try {

        setInitialLoading(true);

        const data =
          await getChatSession(
            paramSessionId
          );

        setSessionId(data.session_id);

        setMessages(
          data.messages || []
        );

      } catch (err) {

        console.error(
          "Failed to load session:",
          err
        );

      } finally {

        setInitialLoading(false);

      }
    };

    loadSession();

  }, [paramSessionId]);

  // =====================================================
  // AUTH CHECK
  // =====================================================

  if (!user) {
    return (
      <Loader message="Authenticating..." />
    );
  }

  // =====================================================
  // SESSION LOADER
  // =====================================================

  if (initialLoading) {
    return (
      <Loader message="Loading previous chat..." />
    );
  }

  // =====================================================
  // SEND MESSAGE
  // =====================================================

  const handleSend = async (
    customInput
  ) => {

    const messageToSend =
      customInput ?? input;

    if (!messageToSend.trim()) return;

    // =====================================
    // ADD USER MESSAGE
    // =====================================

    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        text: messageToSend,
      },
    ]);

    setInput("");

    setLoading(true);

    try {

      const response =
        await sendChatMessage({
          userId: user.id,
          message: messageToSend,
          sessionId,
        });

      // =====================================
      // STORE SESSION ID
      // =====================================

      if (
        response.session_id &&
        !sessionId
      ) {
        setSessionId(
          response.session_id
        );
      }

      // =====================================
      // ADD BOT MESSAGE
      // =====================================

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",

          text:
            response.reply ||
            response.message,

          options:
            response.options || null,

          help:
            response.help || null,

          type:
            response.type || null,

          // IMPORTANT FIX
          prakriti:
            response.prakriti || null,

          predictedRemedy:
            response.predicted_remedy ||
            null,
        },
      ]);

    } catch (error) {

      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text:
            "Sorry, something went wrong. Please try again.",
        },
      ]);

    } finally {

      setLoading(false);

    }
  };

  // =====================================================
  // ENTER KEY
  // =====================================================

  const handleKeyDown = (e) => {

    if (e.key === "Enter") {
      handleSend();
    }

  };

  // =====================================================
  // UI
  // =====================================================

  return (
    <div className="chatbot-page">

      <div className="chatbot-card">

        {/* HEADER */}

        <div className="chatbot-header">
          <h2>
            AyurLife AI Assistant
          </h2>

          <p>
            Ask about symptoms,
            remedies, or Prakriti
          </p>
        </div>

        {/* MESSAGES */}

        <div className="chatbot-messages">

          {messages.length === 0 &&
            !loading && (

            <div className="chatbot-welcome">

              <div className="ai-orb" />

              <h3>
                Welcome to AyurLife
              </h3>

              <p>
                Describe your symptoms
                or type
                <b> Prakriti </b>
                to begin.
              </p>

            </div>
          )}

          {/* CHAT LIST */}

          {messages.map(
            (msg, index) => (

              <MessageBubble
                key={index}

                sender={msg.sender}

                text={msg.text}

                options={msg.options}

                help={msg.help}

                prakriti={
                  msg.prakriti
                }

                predictedRemedy={
                  msg.predictedRemedy
                }

                onOptionClick={(
                  option
                ) =>
                  handleSend(option)
                }
              />
            )
          )}

          {/* TYPING */}

          {loading && (
            <TypingIndicator />
          )}

          <div
            ref={messagesEndRef}
          />

        </div>

        {/* INPUT */}

        <div className="chatbot-input-bar">

          <input
            type="text"

            value={input}

            placeholder="Start typing your symptoms..."

            onChange={(e) =>
              setInput(e.target.value)
            }

            onKeyDown={handleKeyDown}

            disabled={loading}
          />

          <button
            onClick={() =>
              handleSend()
            }
            disabled={loading}
          >
            ➤
          </button>

        </div>

      </div>

    </div>
  );
};

export default Chatbot;