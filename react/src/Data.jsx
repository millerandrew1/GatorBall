import { Link } from "react-router-dom";
import React, { useState, useEffect } from "react";
import "./Data.css";

const Data = () => {
  const [distance, setDistance] = useState(0);
  const [possession, setPossession] = useState("N/A");
  const [lineOfScrimmage, setLineOfScrimmage] = useState("N/A");
  const [currentYardLine, setCurrentYardLine] = useState("N/A");
  const [firstDownMarker, setFirstDownMarker] = useState("N/A");
  const [yardsToGain, setYardsToGain] = useState("N/A");
  const [score, setScore] = useState("N/A");
  const [playClock, setPlayClock] = useState("N/A");
  const [gameClock, setGameClock] = useState("N/A");
  const [quarter, setQuarter] = useState("N/A");

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
      setScore("Home: 14 - Away: 7");
      setPlayClock("25");
      setGameClock("12:35");
      setQuarter("2nd");
      setPossession("Team A");
    }, 3000);

    return () => clearInterval(interval);
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
          <div>
            <strong>Possession:</strong> {possession}
          </div>
          <div>
            <strong>Line of Scrimmage:</strong> {lineOfScrimmage}
          </div>
          <div>
            <strong>Current Yard Line:</strong> {currentYardLine}
          </div>
          <div>
            <strong>First Down Marker:</strong> {firstDownMarker}
          </div>
          <div>
            <strong>Yards To Gain:</strong> {yardsToGain}
          </div>
          <div>
            <strong>Score:</strong> {score}
          </div>
          <div>
            <strong>Play Clock:</strong> {playClock}
          </div>
          <div>
            <strong>Game Clock:</strong> {gameClock}
          </div>
          <div>
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
