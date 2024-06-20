import json
import io
from channels.generic.websocket import AsyncWebsocketConsumer
from stt_app.views.views_v2 import process_audio_stream
from stt_app.deepgram import detect_pauses


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

            # Process audio stream for transcription
            transcription = await process_audio_stream(self.audio_buffer.getvalue())

            # Detect pauses in the current buffer
            pauses = await detect_pauses(self.audio_buffer.getvalue())

            await self.send(text_data=json.dumps({
                'transcription': transcription,
                'pauses': pauses
            }))

            self.audio_buffer = io.BytesIO()