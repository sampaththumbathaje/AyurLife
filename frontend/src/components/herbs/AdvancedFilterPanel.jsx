const AdvancedFilterPanel = ({
  pacify,
  setPacify,
  aggravate,
  setAggravate,
}) => {
  return (
    <aside className="filter-panel">
      <h4>ADVANCED FILTER PANEL</h4>
      <small>(RESEARCH MODE)</small>

      <div className="filter-section">
        <h5>Pacify Dosha</h5>
        {["Vata", "Pitta", "Kapha"].map((d) => (
          <label key={d}>
            <input
              type="checkbox"
              onChange={(e) =>
                setPacify((prev) =>
                  e.target.checked
                    ? [...prev, d]
                    : prev.filter((x) => x !== d)
                )
              }
            />
            {d}
          </label>
        ))}
      </div>

      <div className="filter-section">
        <h5>Aggravate Dosha</h5>
        {["Vata", "Pitta", "Kapha"].map((d) => (
          <label key={d}>
            <input
              type="checkbox"
              onChange={(e) =>
                setAggravate((prev) =>
                  e.target.checked
                    ? [...prev, d]
                    : prev.filter((x) => x !== d)
                )
              }
            />
            {d}
          </label>
        ))}
      </div>
    </aside>
  );
};

export default AdvancedFilterPanel;
