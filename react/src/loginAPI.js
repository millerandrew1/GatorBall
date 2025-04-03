import express from "express";
import cors from "cors";
import fs from "fs";

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 3001;

// Helper function to ensure logins are stored correctly in the JSON file
const saveLoginsToFile = (logins) => {
  fs.writeFile("logins.json", JSON.stringify(logins, null, 2), (err) => {
    if (err) {
      console.error("Error saving logins: ", err);
    }
  });
};

// Load valid GatorBall IDs from a file
const loadValidGatorBallIDs = () => {
  try {
    const data = fs.readFileSync("gatorBallIDs.json", "utf-8");
    return JSON.parse(data); // Return the parsed array of valid IDs
  } catch (error) {
    console.error("Error loading valid GatorBall IDs: ", error);
    return [];
  }
};

app.post("/api/logins", (req, res) => {
  const login = req.body;
  const { username, gatorBallID } = login;

  // Load the valid GatorBall IDs
  const validGatorBallIDs = loadValidGatorBallIDs();

  // Check if the provided GatorBall ID is valid
  if (!validGatorBallIDs.includes(gatorBallID)) {
    return res.status(400).json({ message: "Invalid GatorBall ID" });
  }

  // Read the existing logins.json to check for existing combination
  fs.readFile("logins.json", "utf-8", (err, data) => {
    let logins = [];

    if (err && err.code !== "ENOENT") {
      console.error("Error reading logins.json: ", err);
      return res.status(500).json({ message: "Failed to read logins" });
    }

    // If the file exists and contains data, parse it
    if (data) {
      try {
        logins = JSON.parse(data); // Parse existing logins array
      } catch (parseError) {
        console.error("Error parsing logins data: ", parseError);
        return res.status(500).json({ message: "Failed to parse logins" });
      }
    }

    // Check if the username and gatorBallID combination already exists
    const existingLogin = logins.find(
      (entry) =>
        entry.username === username && entry.gatorBallID === gatorBallID
    );

    // If combination exists, just respond with a successful login
    if (existingLogin) {
      return res.status(200).json({
        message:
          "Login successful, but this combination was already registered.",
      });
    }

    // If combination does not exist, add the new login to the array
    logins.push(login);

    // Save the updated logins array back to the file
    saveLoginsToFile(logins);

    // Respond with success after saving the new login
    res.status(201).json({ message: "Login saved successfully!" });
  });
});

app.get("/api/logins", (req, res) => {
  fs.readFile("logins.json", "utf-8", (err, data) => {
    if (err) {
      console.error("Error reading logins: ", err);
      return res.status(500).json({ message: "Failed to fetch logins" });
    }

    if (!data.trim()) {
      return res.json([]); // Return empty array if no data
    }

    try {
      // Parse and return the existing logins
      const logins = JSON.parse(data);
      res.json(logins);
    } catch (error) {
      console.error("Error parsing logins data: ", error);
      res.status(500).json({ message: "Failed to parse logins data" });
    }
  });
});

app.listen(PORT, () => {
  console.log(`Login server running on port ${PORT}`);
});
