import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import Sidebar from "../common/Sidebar";
import Loader from "../common/Loader";

import { getAllHerbs } from "../../api/herbApi";
import HerbCard from "./HerbCard";

const ITEMS_PER_PAGE = 20;

const HerbList = () => {
  const navigate = useNavigate();

  const [herbs, setHerbs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Pagination
  const [currentPage, setCurrentPage] = useState(1);

  // -----------------------------
  // Fetch All Herbs
  // -----------------------------
  useEffect(() => {
    const fetchHerbs = async () => {
      try {
        setLoading(true);
        const data = await getAllHerbs();
        setHerbs(Array.isArray(data) ? data : data.herbs || []);
      } catch (err) {
        setError(
          err.response?.data?.error ||
            "Failed to load herbs"
        );
      } finally {
        setLoading(false);
      }
    };

    fetchHerbs();
  }, []);

  if (loading) {
    return <Loader message="Loading herbs..." />;
  }

  if (error) {
    return <div>{error}</div>;
  }

  // -----------------------------
  // FILTERED DATASET
  // (Later you can apply search / dosha filters here)
  // -----------------------------
  const filteredHerbs = herbs;

  // -----------------------------
  // Pagination Logic (FIXED)
  // -----------------------------
  const totalPages = Math.ceil(
    filteredHerbs.length / ITEMS_PER_PAGE
  );

  const startIndex =
    (currentPage - 1) * ITEMS_PER_PAGE;

  const endIndex = startIndex + ITEMS_PER_PAGE;

  const currentHerbs = filteredHerbs.slice(
    startIndex,
    endIndex
  );

  const handleNext = () => {
    if (currentPage < totalPages) {
      setCurrentPage((prev) => prev + 1);
      window.scrollTo(0, 0);
    }
  };

  const handlePrevious = () => {
    if (currentPage > 1) {
      setCurrentPage((prev) => prev - 1);
      window.scrollTo(0, 0);
    }
  };

  return (
    <div className="herb-page">
      <Sidebar />

      <main className="herb-grid-section">
        {/* ✅ FIXED COUNT DISPLAY */}

        {/* Herb Grid */}
        <div className="herb-grid">
          {currentHerbs.map((herb) => (
            <HerbCard
              key={herb.herb_id || herb.name}
              herb={herb}
              onClick={() =>
                navigate(
                  `/herbs/${encodeURIComponent(
                    herb.name
                  )}`
                )
              }
            />
          ))}
        </div>

        {/* Pagination Controls */}
        <div className="pagination">
          <button
            onClick={handlePrevious}
            disabled={currentPage === 1}
          >
            Previous
          </button>

          <span>
            Page {currentPage} of {totalPages}
          </span>

          <button
            onClick={handleNext}
            disabled={currentPage === totalPages}
          >
            Next
          </button>
        </div>
      </main>
    </div>
  );
};

export default HerbList;
