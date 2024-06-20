import asyncio
import websockets
import json
from pydantic import BaseModel

class DeepgramService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url = "wss://api.deepgram.com/v1/listen"

    async def transcribe(self, audio_data: bytes):
        async with websockets.connect(
            self.url,
            extra_headers={"Authorization": f"Token {self.api_key}"}
        ) as websocket:
            await websocket.send(audio_data)
            async for message in websocket:
                response = json.loads(message)
                if 'is_final' in response and response['is_final']:
                    return response['channel']['alternatives'][0]['transcript']
        return ""
