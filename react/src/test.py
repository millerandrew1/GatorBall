#can you send me the code real quick for the python stuff where it saves it to the positional value just so i can get some dumby data? im making a test python script where it just creates random data and im gonna connect it to the react app through a websocket and try to get it to work. if it works, ill lyk

from fastapi import FastAPI, WebSocket
import asyncio 

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    count = 0
    x, y, z = 0, 0, 0

    while count < 50:
        data = {"time": x, "yardX": y, "yardY": z}  # Send structured JSON data
        await websocket.send_json(data)  # Send to WebSocket client

        x += 1
        y += 1
        z += 1
        count += 1
        
        await asyncio.sleep(1)  # Adjust as needed for real-time updates

    await websocket.close() 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
