const WebSocket = require("ws");
const express = require("express");
const cors = require("cors");

const app = express();
app.use(cors());

// Start an Express HTTP server (optional, but useful)
const server = app.listen(8080, () => {
  console.log("Server running on http://localhost:8080");
});

// Create WebSocket server on top of the Express server
const wss = new WebSocket.Server({ server });

wss.on("connection", (ws) => {
  console.log("Client connected");

  /* // Send test data every 2 seconds
  setInterval(() => {
    const footballData = {
      x: Math.random() * 100, // Random X position
      y: Math.random() * 50, // Random Y position
      speed: Math.random() * 10, // Speed of the ball
    };
    ws.send(JSON.stringify(footballData));
  }, 2000); */

  // Handle messages from the client
  ws.on("message", (message) => {
    console.log("Received from client:", message);
  });

  // Handle client disconnect
  ws.on("close", () => {
    console.log("Client disconnected");
  });
});
