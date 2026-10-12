import React, { useState } from "react";

import PrakritiChart from "./PrakritiChart";
import InfoModal from "./InfoModal";
import PrakritiDietCard from "./PrakritiDietCard";

import prakritiDietData from "../../data/prakritiDietData";




const MessageBubble = ({
  sender,
  text,
  options,
  help,
  prakriti,
  predictedRemedy,
  onOptionClick,
}) => {

  const isUser = sender === "user";

 



  // =========================================
  // INFO MODAL
  // =========================================

  const [showModal, setShowModal] =
    useState(false);

  // =========================================
  // HELP CONTENT
  // =========================================

  const helpContent =
    help?.descriptions
      ?.map(
        (d) =>
          `${d.label}\n\n${d.text}`
      )
      .join(
        "\n\n━━━━━━━━━━━━━━\n\n"
      ) || "";

  
  // =========================================
  // PRAKRITI CHART
  // =========================================

  const hasChart =
    prakriti &&
    typeof prakriti === "object" &&
    prakriti.probabilities &&
    Object.keys(
      prakriti.probabilities
    ).length > 0;

  // =========================================
  // PRAKRITI DIET DATA
  // =========================================

  const currentDosha =
  prakriti?.prediction
    ?.replace(/\*/g, "")
    ?.split("-")[0]
    ?.trim();

  const prakritiData =
    prakritiDietData.find(
      (item) =>
        item.dosha === currentDosha
    );

  // =========================================
  // UI
  // =========================================

  return (
    <>

      <div
        className={`message-row ${
          isUser
            ? "user"
            : "bot"
        }`}
      >

        <div className="message-bubble">

          {/* =====================================
              MESSAGE TEXT
          ===================================== */}

          {text && (

            <div className="message-text">

              <span>{text}</span>

              {help && (

                <button
                  className="info-btn"
                  onClick={() =>
                    setShowModal(true)
                  }
                >
                  ⓘ More Info
                </button>

              )}

            </div>

          )}

          {/* =========================================
    PRAKRITI CHART + DIET CARD
========================================= */}

{hasChart && (
  <div className="prakriti-result-wrapper">

    {/* Chart */}
    <div className="prakriti-chart-wrapper">
      <PrakritiChart
        probabilities={
          prakriti.probabilities
        }
        prediction={
          prakriti.prediction
        }
      />
    </div>

    {/* Diet Card */}
    {prakritiData && (
      <PrakritiDietCard
        data={prakritiData}
      />
    )}

  </div>
)}

       
          
          

          {/* =====================================
              OPTIONS
          ===================================== */}

          {options?.length > 0 && (

            <div className="options-container">

              {options.map(
                (opt, idx) => (

                  <button
                    key={idx}
                    className="option-chip"
                    onClick={() =>
                      onOptionClick(opt)
                    }
                  >
                    {opt}
                  </button>

                )
              )}

            </div>

          )}

        </div>
      </div>

      {/* =====================================
          INFO MODAL
      ===================================== */}

      <InfoModal
        isOpen={showModal}
        onClose={() =>
          setShowModal(false)
        }
        title="More Information"
        content={helpContent}
      />

    </>
  );
};

export default MessageBubble;