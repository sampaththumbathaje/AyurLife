import React from "react";
import { Link } from "react-router-dom";
import "./Home.css";

const Home = () => {
  return (
    <div className="home-container">

      {/* HERO SECTION */}
      <section className="hero-section">
        <h1>AyurLife – Your Personal Ayurvedic Health Assistant</h1>
        <p>
          An AI-powered Ayurvedic chatbot that combines ancient Indian medical
          wisdom with modern Machine Learning to guide users toward safe,
          natural, and personalized remedies.
        </p>

        <div className="hero-buttons">
          <Link to="/register" className="btn-primary">Get Started</Link>
          <Link to="/login" className="btn-outline">Login</Link>
        </div>
      </section>

      {/* AYURVEDA INTRO */}
      <section className="info-section">
        <h2>Understanding Ancient Ayurveda</h2>
        <p>
          Ayurveda is one of the world’s oldest holistic systems of medicine,
          originating in India over 3,000 years ago. Unlike modern medicine,
          Ayurveda focuses not only on treating diseases but on maintaining
          balance between the body, mind, and lifestyle.
        </p>
        <p>
          Ayurvedic treatment emphasizes natural herbs, dietary regulation,
          daily routines (Dinacharya), and mental well-being. It aims to identify
          the root cause of health issues rather than only suppressing symptoms.
        </p>
      </section>

      {/* PRAKRITI SECTION */}
      <section className="info-section light-bg">
        <h2>What is Prakriti?</h2>
        <p>
          Prakriti refers to an individual’s unique physical and psychological
          constitution, determined at birth. According to Ayurveda, every
          person is governed by three fundamental energies known as Doshas:
          Vata, Pitta, and Kapha.
        </p>

        <ul className="prakriti-list">
          <li><strong>Vata:</strong> Controls movement, energy, and nervous system functions.</li>
          <li><strong>Pitta:</strong> Governs digestion, metabolism, and body temperature.</li>
          <li><strong>Kapha:</strong> Provides strength, stability, and immunity.</li>
        </ul>

        <p>
          Understanding one’s Prakriti helps in choosing the right food,
          lifestyle, and medicines. AyurLife assists users in identifying
          suitable remedies by aligning symptom analysis with Ayurvedic
          principles.
        </p>
      </section>

      {/* HOW TO USE */}
      <section className="info-section">
        <h2>How to Use AyurLife</h2>

        <div className="steps-grid">
          <div className="step-card">
            <h3>1. Register & Login</h3>
            <p>
              Create a secure account to access personalized Ayurvedic
              recommendations and maintain your health history.
            </p>
          </div>

          <div className="step-card">
            <h3>2. Enter Symptoms</h3>
            <p>
              Describe your health concerns in simple language through the
              chatbot interface.
            </p>
          </div>

          <div className="step-card">
            <h3>3. AI-Based Analysis</h3>
            <p>
              The system processes your symptoms using NLP and a trained
              Machine Learning model to predict suitable remedies.
            </p>
          </div>

          <div className="step-card">
            <h3>4. Get Ayurvedic Remedies</h3>
            <p>
              Receive detailed medicine recommendations including ingredients,
              dosage, and precautions.
            </p>
          </div>
        </div>
      </section>

    </div>
  );
};

export default Home;
