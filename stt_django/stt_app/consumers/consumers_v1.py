import json
import io
import os

from dotenv import load_dotenv, find_dotenv

from channels.generic.websocket import AsyncWebsocketConsumer
from stt_app.views.views_v1 import stt, detect_pauses

load_dotenv(find_dotenv())

MOHIR_API_KEY = os.environ.get('API-KEY')

class STTConsumer(AsyncWebsocketConsumer):
    def __init__(self):
        super().__init__()
        self.audio_buffer = io.BytesIO()

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        self.audio_buffer.close()

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            self.audio_buffer.write(bytes_data)

            # Detect pauses in the current buffer
            pauses = detect_pauses(self.audio_buffer.getvalue())

            if pauses:
                self.audio_buffer.seek(0)
                transcription = stt(MOHIR_API_KEY, self.audio_buffer)
                await self.send(text_data=json.dumps({
                    'transcription': transcription,
                    'pauses': pauses
                }))
                self.audio_buffer = io.BytesIO()
