import io
import os

from deepgram import Deepgram

from dotenv import load_dotenv, find_dotenv

DEEPGRAM_API_KEY = os.environ.get('API-KEY')
deepgram = Deepgram(DEEPGRAM_API_KEY)


async def detect_pauses(audio_bytes):
    response = await deepgram.transcription.prerecorded(
        io.BytesIO(audio_bytes),
        {'punctuate': True, 'language': 'uz', 'utterances': True}
    )

    utterances = response['results']['utterances']
    pauses = [{'start': u['start'], 'end': u['end']} for u in utterances if u['is_final']]
    return pauses