import express from "express";
import cors from "cors";
import fs from "fs";

const app = express();
app.use(cors());
app.use(express.json());
const PORT = process.env.PORT || 3002;

const FILE_PATH = "gameStates.json";
let gameStates = [];

fs.readFile(FILE_PATH, "utf-8", (err, data) => {
  if (!err && data) {
    try {
      gameStates = JSON.parse(data);
    } catch (parseError) {
      console.error("Error parsing existing game states: ", parseError);
      gameStates = []; // Reset to empty if there's a parsing issue
    }
  }
});

// Save game states to file
const saveStatesToFile = () => {
  fs.writeFile(FILE_PATH, JSON.stringify(gameStates, null, 2), (err) => {
    if (err) {
      console.error("Error saving game states: ", err);
    } else {
      console.log("Game states saved successfully!");
    }
  });
};

// Save game states periodically every 5 seconds
setInterval(saveStatesToFile, 5000);

// API endpoint to receive game states
app.post("/api/game-states", (req, res) => {
  const { gameStates: newStates } = req.body;

  if (!Array.isArray(newStates) || newStates.length === 0) {
    return res.status(400).json({ message: "Invalid game state data" });
  }

  gameStates.push(...newStates); // Append new states to in-memory storage
  res.status(201).json({ message: "Game states received!" });
});

// API endpoint to get all game states
app.get("/api/game-states", (req, res) => {
  res.json(gameStates);
});

app.listen(PORT, () => {
  console.log(`Game State server running on port ${PORT}`);
});

{
  /*const saveStatesToFile = (states) => {
  fs.writeFile("gameStates.json", JSON.stringify(states, null, 2), (err) => {
    if (err) {
      console.error("Error saving game state: ", err);
      return res.status(500).json({ message: "Failed to save game state" });
    }
    console.log("Game state saved successfully!");
    res.status(201).json({ message: "Game state saved successfully!" });
  });
};

app.post("/api/game-states", (req, res) => {
  const state = req.body;

  fs.readFile("gameStates.json", "utf-8", (err, data) => {
    let states = [];

    if (err && err.code !== "ENOENT") {
      console.error("Error reading gameStates.json: ", err);
      return res.status(500).json({ message: "Failed to read game states" });
    }

    if (data) {
      try {
        states = JSON.parse(data);
      } catch (parseError) {
        console.error("Error parsing logins data: ", parseError);
        return res.status(500).json({ message: "Failed to parse game states" });
      }
    }

    states.push(state);
    saveStatesToFile(states, res);
    
  });
});

app.get("/api/game-states", (req, res) => {
  fs.readFile("gameStates.json", "utf-8", (err, data) => {
    if (err) {
      console.error("Error reading states: ", err);
      return res.status(500).json({ message: "Failed to fetch game states" });
    }

    if (!data.trim()) {
      return res.json([]);
    }

    try {
      const states = JSON.parse(data);
      res.json(states);
    } catch (error) {
      console.error("Error parsing game state data: ", error);
      res.status(500).json({ message: "Failed to parse game state data" });
    }
  });
});

app.listen(PORT, () => {
  console.log(`Game State server running on port ${PORT}`);
}); */
}
