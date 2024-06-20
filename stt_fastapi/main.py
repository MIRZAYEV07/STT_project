import os

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from websocket_manager import ConnectionManager
from stt_service import STTService
from deepgram_service import DeepgramService

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

API_KEY = os.environ.get('API-KEY')

app = FastAPI()
manager = ConnectionManager()
stt_service = STTService(api_key=API_KEY )
deepgram_service = DeepgramService(api_key=API_KEY )

@app.get("/")
async def get():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>WebSocket Audio Stream</title>
    </head>
    <body>
        <h1>WebSocket Audio Stream</h1>
        <button onclick="startRecording()">Start Recording</button>
        <button onclick="stopRecording()">Stop Recording</button>
        <script>
            var ws;
            function startRecording() {
                ws = new WebSocket("ws://localhost:8000/ws");
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                ws.onopen = function(event) {
                    ws.send("Start streaming");
                };
            }
            function stopRecording() {
                ws.close();
            }
        </script>
        <ul id="messages"></ul>
    </body>
    </html>
    """
    return HTMLResponse(html_content)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_bytes()
            file_path = save_audio(data)
            stt_result = stt_service.transcribe(file_path)
            pause_detection_result = await deepgram_service.transcribe(data)
            if pause_detection_result:
                await manager.send_personal_message(pause_detection_result, websocket)
            else:
                await manager.send_personal_message(stt_result.text, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

def save_audio(audio_data: bytes) -> str:
    file_path = "audio_temp.wav"
    with open(file_path, "wb") as f:
        f.write(audio_data)
    return file_path
