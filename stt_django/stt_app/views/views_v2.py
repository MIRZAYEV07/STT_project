import os

import requests
import io

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

MOHIR_API_KEY = os.environ.get('API-KEY')
MOHIR_URL = 'https://mohir.ai/api/v1/stt'

def stt(api_key, audio_buffer):
    headers = {
        "Authorization": api_key
    }

    files = {
        "file": ("audio.mp3", audio_buffer),
    }
    data = {
        "return_offsets": "true",
        "run_diarization": "false",
        "language": "uz",
        "blocking": "true",
    }

    try:
        response = requests.post(MOHIR_URL, headers=headers, files=files, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Request failed with status code {response.status_code}: {response.text}"
    except requests.exceptions.Timeout:
        return "Request timed out. The API response took too long to arrive."

async def process_audio_stream(audio_bytes):
    audio_buffer = io.BytesIO(audio_bytes)
    transcription = stt(MOHIR_API_KEY, audio_buffer)
    return transcription