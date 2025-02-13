import { useState } from "react";
import { Link } from "react-router-dom";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";

function App() {
  const [count, setCount] = useState(0);
  const [text, setText] = useState("");

  return (
    <>
      <header className="header">
        <a href="https://www.youtube.com/watch?v=xvFZjo5PgG0" target="_blank">
          <img src="src/assets/uf.png" className="logo" alt="UF Logo" />
        </a>
        <h1>GatorBall</h1>
      </header>

      <div className="code">
        <h3>Insert GatorBall ID: </h3>
        <input
          type="password"
          placeholder="Enter text here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <p>You typed (just to check): {text}</p>
      </div>

      <nav>
        <Link to="/data">Login</Link>
      </nav>

      <p className="read-the-docs">Click on the UF logo to learn more</p>
    </>
  );
}

export default App;
