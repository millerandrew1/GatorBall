{
  /*This is back on the drawing block, want to convert the logins to csv file*/
}

{
  /*import fs from "fs";
import axios from "axios";

async function fetchAndSave() {
  try {
    const response = await axios.get("http://localhost:3001/api/logins");
    const data = response.data;

    // Read the existing logins from the logins.json file if it exists
    let existingLogins = [];
    if (fs.existsSync("logins.json")) {
      const fileData = fs.readFileSync("logins.json", "utf-8");
      // Parse existing data, handle the case where the file is empty
      try {
        existingLogins = JSON.parse(fileData);
      } catch (err) {
        console.log("logins.json is empty or corrupted, starting fresh.");
      }
    }

    // Append the new logins to the existing logins array
    existingLogins = [...existingLogins, ...data];

    fs.writeFileSync("logins.json", JSON.stringify(data, null, 2));

    const csvFilePath = "logins.csv";
    const csvHeaders = "username, gator_ball_id\n";

    if (!fs.existsSync(csvFilePath)) {
      fs.writeFileSync(csvFilePath, csvHeaders);
    }
    data.forEach((login) => {
      const csvRow = `${data.username},${data.gator_ball_id}\n`;
      fs.appendFileSync(csvFilePath, csvRow);
    });

    console.log("Logins saved successfully!");
  } catch (error) {
    console.error("Error fetching login data: ", error);
  }
}

setInterval(fetchAndSave, 5000);*/
}
