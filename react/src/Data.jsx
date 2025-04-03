import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import React, { useState, useEffect } from "react";
import "./Data.css";

const Data = ({ data }) => {
  const [CYL, setCYL] = useState(25);
  const [LOS, setLOS] = useState(25);
  const [FD, setFD] = useState(35);
  const [yardsToGain, setYardsToGain] = useState(10);
  const [down, setDown] = useState(1);
  const [currentYardLine, setCurrentYardLine] = useState("25 yard-line");
  const [lineOfScrimmage, setLineOfScrimmage] = useState("25 yard-line");
  const [firstDownMarker, setFirstDownMarker] = useState("35 yard-line");
  const [downAndYardage, setDownAndYardage] = useState("1st & 10");
  const [possession, setPossession] = useState("Team A");
  const [score, setScore] = useState({ home: 0, away: 0 });
  const [quarter, setQuarter] = useState(1);
  const [clock, setClock] = useState("0:00");
  const [error, setError] = useState("");

  const [applyLOS, setApplyLOS] = useState(0);
  const [applyFD, setApplyFD] = useState(0);
  const applyYardage = () => {
    const los = Number(applyLOS);
    const fd = Number(applyFD);
    if (los < 1 || los > 100 || fd < 1 || fd > 100) {
      setError("Please enter numbers between 1 and 99");
      return;
    } else if (fd <= los) {
      setError("Make sure the first down marker is past the line of scrimmage");
      return;
    }

    setError("");
    setLOS(applyLOS);
    setFD(applyFD);
    setLineOfScrimmage(`${applyLOS} yard-line`);
    setFirstDownMarker(`${applyFD} yard-line`);
  };

  const incrementDown = () => {
    if (down < 4) {
      setDown(down + 1);
    } else {
      setDown(1);
      flip();
    }
  };

  const undoDown = () => {
    if (down == 1) {
      setDown(4);
      flip();
    } else {
      setDown(down - 1);
    }
  };

  const [isFlipped, setIsFlipped] = useState(false);
  const flip = () => {
    setIsFlipped((prev) => !prev);
    setPossession((prev) => (prev === "Team A" ? "Team B" : "Team A"));
  };

  const [homeScore, setHomeScore] = useState(0);
  const [awayScore, setAwayScore] = useState(0);
  const [lastScore, setLastScore] = useState(null);
  const applyScore = () => {
    const home = Number(homeScore);
    const away = Number(awayScore);
    setLastScore({ ...score });
    if (home < 0 || home > 100 || away < 0 || home > 100) {
      setError("Please enter numbers between 0 and 100");
      return;
    }
    setScore({ home: home, away: away });
    setHomeScore("");
    setAwayScore("");
    setError("");
  };

  const incrementQuarter = () => {
    if (quarter < 4) {
      setQuarter(quarter + 1);
    } else {
      flip();
      setPossession("Team B");
    }
  };

  const handleScore = (event, team) => {
    const temp = parseInt(event.target.value, 10);
    console.log(team);
    console.log(event);
    console.log(temp);
    setLastScore({ ...score });
    setScore((prevScore) => ({
      ...prevScore,
      [team]: prevScore[team] + temp,
    }));
    event.target.value = "";
  };

  const undoLastScore = () => {
    if (lastScore) {
      setScore(lastScore);
      setLastScore(null);
    }
  };

  const reset = () => {
    setLOS(25);
    setFD(35);
    setYardsToGain(10);
    setDown(1);
    setCurrentYardLine("25 yard-line");
    setLineOfScrimmage("25 yard-line");
    setFirstDownMarker("35 yard-line");
    setDownAndYardage("1st & 10");
    setPossession("Team A");
    setScore({ home: 0, away: 0 });
    setQuarter(1);
    setClock("0:00");
    setError("");
    setApplyLOS(0);
    setApplyFD(0);
    setHomeScore(0);
    setAwayScore(0);
    setLastScore(null);
  };

  const [logout, setLogout] = useState(false);
  const navigate = useNavigate();
  const handleLogout = () => {
    setLogout(true);
  };

  const [position, setPosition] = useState({ x: 0, y: 0, z: 0 });

  useEffect(() => {
    const socket = new WebSocket("ws://localhost:8000/ws");

    socket.onopen = () => console.log("WebSocket Connected");
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setPosition(data);
    };

    socket.onclose = () => console.log("WebSocket Disconnected");

    return () => socket.close(); // Cleanup on component unmount
  }, []);

  useEffect(() => {
    setYardsToGain(FD - LOS);
    if (down === 1) {
      setDownAndYardage(`1st & ${yardsToGain}`);
    } else if (down === 2) {
      setDownAndYardage(`2nd & ${yardsToGain}`);
    } else if (down === 3) {
      setDownAndYardage(`3rd & ${yardsToGain}`);
    } else if (down === 4) {
      setDownAndYardage(`4th & ${yardsToGain}`);
    }
  });

  useEffect(() => {
    if (logout) {
      navigate("/");
    }
  }, [logout, navigate]);

  return (
    <>
      <header className="title">
        <a href="https://www.ufl.edu/" target="_blank">
          <img src="src/assets/uf.png" className="uf-logo" alt="UF Logo" />
        </a>
        <h1>GatorBall</h1>
        <nav>
          <button className="logout-button" onClick={handleLogout}>
            Sign Out
          </button>
        </nav>
      </header>
      <section className="body">
        <div className="main">
          <div className="field">
            <div className="left-end-zone">ENDZONE</div>
            <div className="main-field">
              <div className="yard-lines">
                {[10, 20, 30, 40, 50, 40, 30, 20, 10].map((yard, index) => (
                  <div key={index} className="yard-line">
                    <span className="yard-number">{yard}</span>
                  </div>
                ))}
              </div>
              <div
                className="current-yard-line"
                style={{
                  left: `${CYL - 0.5}%`,
                }}
              ></div>
              <div
                className="line-of-scrimmage"
                style={{
                  left: isFlipped ? `${100 - LOS}%` : `${LOS}%`,
                }}
              ></div>
              <div
                className="first-down-marker"
                style={{
                  left: isFlipped ? `${100 - FD}%` : `${FD}%`,
                }}
              ></div>
            </div>
            <div className="right-end-zone">ENDZONE</div>
          </div>

          <div className="info">
            <div className="info-section set-LOS-and-FD">
              <strong>Set Line of Scrimmage & First Down: </strong>
              <input
                type="number"
                placeholder="Line of Scrimmage (e.g., 30)"
                value={applyLOS || ""}
                onChange={(e) => setApplyLOS(e.target.value)}
                className="custom-yard-input"
              />
              <input
                type="number"
                placeholder="First Down (e.g., 30)"
                value={applyFD || ""}
                onChange={(e) => setApplyFD(e.target.value)}
                className="custom-yard-input"
              />
              {error && <p>{error}</p>}
              <button onClick={applyYardage} className="applyYardage">
                Apply
              </button>
            </div>
            <div className="info-section">
              <strong>Current Yard Line: </strong>
              {currentYardLine}
            </div>
            <div className="info-section">
              <strong>Line of Scrimmage: </strong>
              {lineOfScrimmage}
            </div>
            <div className="info-section">
              <strong>First Down Marker: </strong>
              {firstDownMarker}
            </div>
            <div className="info-section">
              <strong>Down:</strong> {downAndYardage}{" "}
              <button className="down-button" onClick={incrementDown}>
                Increment Down
              </button>
              <button className="down-button" onClick={undoDown}>
                Undo Down
              </button>
            </div>
            <div className="info-section possession-section">
              <strong>Possession: </strong>
              {possession}
              <button className="flip button" onClick={flip}>
                Swap Possession
              </button>
            </div>
            <div className="info-section">
              <strong>Score:</strong> Home {score.home} - Away {score.away}
            </div>
            <div className="info-section score-panel">
              <label className="homeScore">
                <strong>Home Team:</strong>
                <select
                  className="dropdown"
                  name="score"
                  defaultValue=""
                  onChange={(e) => handleScore(e, "home")}
                >
                  <option id="score-holder" value="" disabled>
                    Select Scoring Option
                  </option>
                  <option value="6">Touchdown (6)</option>
                  <option value="1">PAT (1)</option>
                  <option value="3">FG (3)</option>
                  <option value="2">Safety (2)</option>
                  <option value="2">2PT Conversion (2)</option>
                </select>
              </label>
              <label className="awayScore">
                <strong>Away Team:</strong>
                <select
                  className="dropdown"
                  name="score"
                  defaultValue=""
                  onChange={(e) => handleScore(e, "away")}
                >
                  <option id="score-holder" value="" disabled>
                    Select Scoring Option
                  </option>
                  <option value="6">Touchdown (6)</option>
                  <option value="1">PAT (1)</option>
                  <option value="3">FG (3)</option>
                  <option value="2">Safety (2)</option>
                  <option value="2">2PT Conversion (2)</option>
                </select>
              </label>
              <button className="undo-score" onClick={undoLastScore}>
                Undo Last Score
              </button>
            </div>
            <div className="info-section set-score">
              <strong>Set Score:</strong>
              <input
                type="number"
                placeholder="Home Team Score"
                value={homeScore || ""}
                onChange={(e) => setHomeScore(e.target.value)}
                className="custom-score-input"
              />
              <input
                type="number"
                placeholder="Away Team Score"
                value={awayScore || ""}
                onChange={(e) => setAwayScore(e.target.value)}
                className="custom-score-input"
              />
              {error && <p>{error}</p>}
              <button onClick={applyScore} className="applyScore">
                Apply
              </button>
            </div>
            <div className="info-section">
              <strong>Quarter: </strong>
              {quarter}{" "}
              <button className="quarter-button" onClick={incrementQuarter}>
                Next Quarter
              </button>
            </div>
            <div className="info-section">
              <strong>Game Clock: </strong>
              {clock}
            </div>
            <div className="info-section">
              <button className="reset-button" onClick={reset}>
                Reset Game
              </button>
            </div>
          </div>
        </div>
      </section>
      <div>
        <h1>Real-Time Position</h1>
        <p>X: {position.x}</p>
        <p>Y: {position.y}</p>
        <p>Z: {position.z}</p>
      </div>
    </>
  );
};

export default Data;
