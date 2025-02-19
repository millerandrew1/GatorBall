import { Link } from "react-router-dom";
import React, { useState, useEffect, useRef } from "react";
import "./Data.css";

const Data = () => {
  const [distance, setDistance] = useState(0);
  const [possession, setPossession] = useState("N/A");
  const [lineOfScrimmage, setLineOfScrimmage] = useState("N/A");
  const [currentYardLine, setCurrentYardLine] = useState("N/A");
  const [firstDownMarker, setFirstDownMarker] = useState("N/A");
  const [yardsToGain, setYardsToGain] = useState("N/A");
  const [score, setScore] = useState({ home: 0, away: 0 });
  const [playClock, setPlayClock] = useState("N/A");
  const [gameClock, setGameClock] = useState("N/A");
  const [quarter, setQuarter] = useState("N/A");
  const [lastScore, setLastScore] = useState(null);
  const [dropdownOpen, setDropdownOpen] = useState({
    home: false,
    away: false,
  });

  const homeDropdownRef = useRef(null);
  const awayDropdownRef = useRef(null);

  useEffect(() => {
    // Simulate dynamic updates (replace with actual data fetching)
    const interval = setInterval(() => {
      const randomYards = Math.random() * 100;
      const currentYards =
        randomYards > 50
          ? 100 - Math.floor(randomYards)
          : Math.floor(randomYards);
      const firstDownYards =
        randomYards + 10 > 50
          ? 100 - Math.floor(randomYards + 10)
          : Math.floor(randomYards + 10);

      const outcome =
        firstDownYards <= 0 || firstDownYards >= 100
          ? "TOUCHDOWN"
          : `${Math.floor(firstDownYards)}-yard line`;

      setDistance(randomYards);
      setLineOfScrimmage(`${Math.floor(currentYards)}-yard line`);
      setCurrentYardLine(`${Math.floor(currentYards)}-yard line`);
      setFirstDownMarker(outcome);
      setYardsToGain("10 yards");
      {
        /*setScore("Home: 14 - Away: 7");*/
      }
      setPlayClock("25");
      setGameClock("12:35");
      setQuarter("2nd");
      setPossession("Team A");
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  const scoringOptions = [
    { label: "Touchdown (6)", points: 6 },
    { label: "Extra Point (1)", points: 1 },
    { label: "Two-Point Conversion (2)", points: 2 },
    { label: "Field Goal (3)", points: 3 },
    { label: "Safety (2)", points: 2 },
  ];

  const toggleDropdown = (team) => {
    setDropdownOpen((prev) => ({
      home: team === "home" ? !prev.home : false,
      away: team === "away" ? !prev.away : false,
    }));
  };

  const updateScore = (team, points) => {
    setScore((prev) => {
      const newScore = { ...prev, [team]: prev[team] + points };
      setLastScore({ team, points });
      return newScore;
    });
    setDropdownOpen({ home: false, away: false });
  };

  const undoLastScore = () => {
    if (lastScore) {
      setScore((prev) => ({
        ...prev,
        [lastScore.team]: prev[lastScore.team] - lastScore.points,
      }));
      setLastScore(null);
    }
  };

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        homeDropdownRef.current &&
        !homeDropdownRef.current.contains(event.target) &&
        awayDropdownRef.current &&
        !awayDropdownRef.current.contains(event.target)
      ) {
        setDropdownOpen({ home: false, away: false });
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  return (
    <>
      <div className="football-container">
        {/* Football Field */}
        <div className="field">
          {/* Left End Zone */}
          <div className="end-zone left">GATORS</div>

          {/* Play Area */}
          <div className="play-area">
            {/* Yard Lines */}
            {/* Yard Lines */}
            <div className="yard-lines">
              {["10", "20", "30", "40", "50", "40", "30", "20", "10"].map(
                (yard, i) => (
                  <div key={i} className="yard-line-container">
                    <div className="yard-line"></div>
                    <div className="yard-marker">{yard}</div>
                  </div>
                )
              )}
            </div>

            {/* First Down Marker */}
            <div
              className="first-down-marker"
              style={{ left: `${distance + 10}%` }}
            ></div>

            {/* Current Yard Marker */}
            <div
              className="current-yard-marker"
              style={{ left: `${distance}%` }}
            ></div>
          </div>

          {/* Right End Zone */}
          <div className="end-zone right">GATORS</div>
        </div>

        {/* Game Info */}
        <div className="info-panel">
          <div className="info-section">
            <strong>Possession:</strong> {possession}
          </div>
          <div className="info-section">
            <strong>Line of Scrimmage:</strong> {lineOfScrimmage}
          </div>
          <div className="info-section">
            <strong>Current Yard Line:</strong> {currentYardLine}
          </div>
          <div className="info-section">
            <strong>First Down Marker:</strong> {firstDownMarker}
          </div>
          <div className="info-section">
            <strong>Yards To Gain:</strong> {yardsToGain}
          </div>
          <div className="info-section">
            <strong>Score:</strong> Home {score.home} - Away {score.away}
          </div>

          {/*Score Buttons*/}
          <div className="score-container">
            {/* Home Score Dropdown */}
            <div className="dropdown" ref={homeDropdownRef}>
              <button
                className="scoreButton"
                onClick={() => toggleDropdown("home")}
              >
                Home Score
              </button>
              {dropdownOpen.home && (
                <div className="dropdown-content">
                  {scoringOptions.map((option, index) => (
                    <button
                      key={index}
                      className="scoreOption"
                      onClick={() => updateScore("home", option.points)}
                    >
                      {option.label}
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Away Score Dropdown */}
            <div className="dropdown" ref={awayDropdownRef}>
              <button
                className="scoreButton"
                onClick={() => toggleDropdown("away")}
              >
                Away Score
              </button>
              {dropdownOpen.away && (
                <div className="dropdown-content">
                  {scoringOptions.map((option, index) => (
                    <button
                      key={index}
                      className="scoreOption"
                      onClick={() => updateScore("away", option.points)}
                    >
                      {option.label}
                    </button>
                  ))}
                </div>
              )}
            </div>

            <button className="undoButton undo" onClick={undoLastScore}>
              Undo Last Score
            </button>
          </div>

          <div className="info-section">
            <strong>Play Clock:</strong> {playClock}
          </div>
          <div className="info-section">
            <strong>Game Clock:</strong> {gameClock}
          </div>
          <div className="info-section">
            <strong>Quarter:</strong> {quarter}
          </div>
        </div>
      </div>
      <h2>FOOTBALL FIELD</h2>
      <Link to="/">Logout</Link>
    </>
  );
};

export default Data;
