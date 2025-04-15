# can you send me the code real quick for the python stuff where it saves it to the positional value just so i can get some dumby data? im making a test python script where it just creates random data and im gonna connect it to the react app through a websocket and try to get it to work. if it works, ill lyk

import json
from pathlib import Path
from fastapi import FastAPI, WebSocket
import asyncio 
from threading import Lock
import time
from datetime import datetime

file = Path("gameStates.json")

# Ensure the file exists and is initialized properly with an empty list
if not file.exists():
    file.write_text("[]")

# Create a lock to avoid concurrency issues
file_lock = Lock()

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    count = 0
    x = 0
    y = 0
    z= 0

    while count < 50:
        data = {"time": x, "yardX": y, "yardY": z}  # Send structured JSON data
        await websocket.send_json(data)  # Send to WebSocket client

        try:
            with file_lock:
                # Read current content of the file
                with file.open("r") as f:
                    try:
                        existing_data = json.load(f)
                        if not isinstance(existing_data, list):
                            existing_data = []  # Reset if the file content is not a list
                    except json.JSONDecodeError:
                        existing_data = []  # If JSON is corrupted, reset it

                # Append new data to the list
                existing_data.append(data)

                # Write the updated data back to the file
                with file.open("w") as f:
                    json.dump(existing_data, f, indent=2)

        except Exception as e:
            print(f"Error writing to JSON file: {e}")


        """
        try:
            exist = json.loads(file.read_text())
            exist.append(data)
            file.write_text(json.dumps(exist, indent=2))
        except Exception as e:
            print(f"Failed to write to JSON file: {e}")
        """

        now = datetime.now()
        x = time.strftime("%H:%M:%S") + f".{now.microsecond // 1000:03d}"       
        y = 1
        z = 0
        count += 1
        await asyncio.sleep(1)  # Adjust as needed for real-time updates

    await websocket.close() 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
