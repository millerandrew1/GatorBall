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
