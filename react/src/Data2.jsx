import { Link } from "react-router-dom";
import React, { useState, useEffect, useRef } from "react";
import "./Data.css";

const Data = () => {
  const [distance, setDistance] = useState(0);
  const [down, setDown] = useState(1);
  const [possession, setPossession] = useState("Team A");
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
  const [isFlipped, setIsFlipped] = useState(false);

  const homeDropdownRef = useRef(null);
  const awayDropdownRef = useRef(null);

  // New input states for user-defined line of scrimmage and first down
  const [inputLOS, setInputLOS] = useState("");
  const [inputFirstDown, setInputFirstDown] = useState("");

  const ws = useRef(null);

  useEffect(() => {
    ws.current = new WebSocket("ws://localhost:8080"); // Update with actual WebSocket URL

    ws.current.onopen = () => {
      console.log("WebSocket connected");
    };

    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === "update") {
        setDistance(data.distance || distance);
        setDown(data.down || down);
        setPossession(data.possession || possession);
        setLineOfScrimmage(data.lineOfScrimmage || lineOfScrimmage);
        setCurrentYardLine(data.currentYardLine || currentYardLine);
        setFirstDownMarker(data.firstDownMarker || firstDownMarker);
        setYardsToGain(data.yardsToGain || yardsToGain);
        setScore(data.score || score);
        setPlayClock(data.playClock || playClock);
        setGameClock(data.gameClock || gameClock);
        setQuarter(data.quarter || quarter);
      }
    };

    ws.current.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    ws.current.onclose = () => {
      console.log("WebSocket disconnected");
    };

    return () => {
      ws.current.close();
    };
  }, []);

  useEffect(() => {
    // Simulate dynamic updates (replace with actual data fetching)
    const interval = setInterval(() => {
      const randomYards = Math.floor(Math.random() * 100);
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

      const goal =
        randomYards <= 40 || randomYards >= 50
          ? Math.abs(firstDownYards - currentYards)
          : 50 - currentYards + (50 - firstDownYards);

      const goalCheck = outcome == "TOUCHDOWN" ? "Goal" : goal;
      const finalGoal = down + "st & " + goalCheck;
      setDistance(randomYards);
      setLineOfScrimmage(`${Math.floor(currentYards)}-yard line`);
      setCurrentYardLine(`${Math.floor(currentYards)}-yard line`);
      setFirstDownMarker(outcome);
      setYardsToGain(`${finalGoal}`);
      setPlayClock("25");
      setGameClock("12:35");
      setQuarter("2nd");
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

  const flip = () => {
    setIsFlipped((prev) => !prev);
    setPossession((prev) => (prev === "Team A" ? "Team B" : "Team A"));
  };

  const incrementDown = () => {};

  const applyMarkers = () => {
    if (inputLOS) {
      setLineOfScrimmage(`${inputLOS}-yard line`);
      setCurrentYardLine(`${inputLOS}-yard line`);
      setDistance(parseInt(inputLOS));
    }
    if (inputFirstDown) {
      setFirstDownMarker(`${inputFirstDown}-yard line`);
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
            <div className="horizontal-yard-lines">
              {[10, 20, 30, 40, 50, 40, 30, 20, 10].map((yard, index) => (
                <div key={index} className="horizontal-yard-line">
                  <span className="yard-number">{yard}</span>
                </div>
              ))}
            </div>

            {/* First Down Marker */}
            <div
              className="first-down-marker"
              style={{
                left: isFlipped
                  ? `${100 - (distance + 10)}%`
                  : `${distance + 10}%`,
              }}
            ></div>

            {/* Current Yard Marker */}
            <div
              className="current-yard-marker"
              style={{
                left: isFlipped ? `${100 - distance}%` : `${distance}%`,
              }}
            ></div>
          </div>

          {/* Right End Zone */}
          <div className="end-zone right">GATORS</div>
        </div>

        {/* Game Info */}
        <div className="info-panel">
          {/* Custom Line of Scrimmage and First Down Input */}
          <div className="info-section">
            <strong>Set Line of Scrimmage & First Down:</strong>
            <input
              type="number"
              placeholder="Line of Scrimmage (e.g., 30)"
              value={inputLOS}
              onChange={(e) => setInputLOS(e.target.value)}
              className="custom-input"
            />
            <input
              type="number"
              placeholder="First Down (e.g., 40)"
              value={inputFirstDown}
              onChange={(e) => setInputFirstDown(e.target.value)}
              className="custom-input"
            />
            <button onClick={applyMarkers} className="applyButton">
              Apply
            </button>
          </div>
          <div className="info-section possession-section">
            <strong>Possession:</strong> {possession}
            <button className="scoreButton flipButton" onClick={flip}>
              Flip Possession
            </button>
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
            <strong>Down:</strong> {yardsToGain}
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
