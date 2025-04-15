import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import "./App.css";

function App() {
  const [username, setUsername] = useState("");
  const [gatorBallID, setGatorBallID] = useState("");
  const [loginSuccess, setLoginSuccess] = useState(false);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const tempLogin = () => {
    setLoginSuccess(true);
  };

  const saveLogin = async (e) => {
    e.preventDefault();
    console.log(`Username: ${username} \n Password: ${gatorBallID}`);

    const login = {
      username,
      gatorBallID,
    };

    try {
      const response = await axios.post(
        "http://localhost:3001/api/logins",
        login
      );
      console.log("Login saved!", response);
      setError("");
      setLoginSuccess(true);
    } catch (error) {
      if (error.response && error.response.status === 400) {
        console.error("Invalid GatorBall ID.");
        setError("Invalid GatorBall ID");
      }
      console.error("Error saving login: ", error);
    }
  };

  useEffect(() => {
    if (loginSuccess) {
      navigate("/data");
    }
  }, [loginSuccess, navigate]);

  return (
    <>
      <header className="header">
        <a href="https://www.ufl.edu/" target="_blank">
          <img src="src/assets/uf.png" className="uf-logo" alt="UF Logo" />
        </a>
        <h1>GatorBall</h1>
      </header>

      <form className="login" onSubmit={saveLogin}>
        <h2>Create Account: </h2>
        <input
          requiretemp
          className="login-bar"
          type="text"
          placeholder="Create Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          required
          className="login-bar gatorball-id"
          type="password"
          placeholder="Insert Gatorball ID"
          value={gatorBallID}
          onChange={(e) => setGatorBallID(e.target.value)}
        />
        {error && <p>{error}</p>}
        <button type="submit" className="login-button">
          Login
        </button>
      </form>

      <p className="click-logo">
        Click on the UF Logo to access organizations home page
      </p>
    </>
  );
}

export default App;
