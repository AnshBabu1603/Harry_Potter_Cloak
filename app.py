from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

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
    import subprocess
    subprocess.Popen(["python", "cloak_ai_gpu.py"])
    return {"message": "Cloak started! Check your Python window for the live cloak feed."}

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # Here you can send real-time data from your cloak system
            await websocket.send_text(f"Message received: {data}")
    except Exception as e:
        print("WebSocket connection closed:", e)
