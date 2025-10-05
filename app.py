from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import subprocess
import asyncio

app = FastAPI()

# ----------------- HTTP Routes ----------------- #
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>Harry Potter Invisibility Cloak</title>
        </head>
        <body style="text-align:center; font-family:sans-serif;">
            <h1>🧙‍♂️ Harry Potter Invisibility Cloak</h1>
            <p>Click the button below to start the cloak system (press 'q' to quit the cloak window).</p>
            <form action="/start">
                <button style="padding:10px 20px; font-size:16px;">Start Cloak</button>
            </form>
        </body>
    </html>
    """

@app.get("/start")
def start_cloak():
    """
    Starts the cloak system as a separate Python process.
    """
    subprocess.Popen(["python", "cloak_ai_gpu.py"])
    return {"message": "Cloak started! Check your Python window for the live cloak feed."}

# ----------------- WebSocket Route ----------------- #
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Handles WebSocket connections for real-time status updates.
    """
    await websocket.accept()
    print("WebSocket connection accepted")
    try:
        while True:
            # Receive message from frontend
            data = await websocket.receive_text()
            
            # Here, you can integrate real-time data from your cloak system if needed
            # For now, it just echoes the message back
            response = f"Server received: {data}"
            
            # Send message back to frontend
            await websocket.send_text(response)

            # Optional: send periodic status updates
            # await websocket.send_text("Cloak is running...")

            # Sleep briefly to avoid blocking
            await asyncio.sleep(0.01)
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print("WebSocket error:", e)

# ----------------- Run Instructions ----------------- #
# Make sure to run this with:
# uvicorn app:app --host 0.0.0.0 --port 10000
# And install dependencies:
# pip install fastapi "uvicorn[standard]" websockets
