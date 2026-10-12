import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { registerUser } from "../../api/authApi";
import Loader from "../common/Loader";

const Register = () => {
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!name || !email || !password) {
      setError("All fields are required");
      return;
    }

    if (password.length < 6) {
      setError("Password must be at least 6 characters");
      return;
    }

    try {
      setLoading(true);
      await registerUser({ name, email, password });
      navigate("/login");
    } catch (err) {
      setError(
        err.response?.data?.error ||
          "Registration failed. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <Loader message="Creating account..." />;
  }

  return (
  <div className="auth-page">
    <div className="auth-card">
      <h2 className="auth-title">Create Your AyurLife Account</h2>
      <p className="auth-subtitle">
        Begin your journey toward holistic Ayurvedic wellness
      </p>

      {error && (
        <p className="auth-error">{error}</p>
      )}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Full Name</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Enter your full name"
          />
        </div>

        <div className="form-group">
          <label>Email Address</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Enter your email"
          />
        </div>

        <div className="form-group">
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Create a password"
          />
        </div>

        <button type="submit" className="auth-btn">
          Register
        </button>
      </form>

      <p className="auth-footer">
        Already have an account?{" "}
        <Link to="/login">Login here</Link>
      </p>
    </div>
  </div>
);

};

export default Register;
