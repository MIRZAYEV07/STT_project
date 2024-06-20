import requests
from pydantic import BaseModel

class STTResult(BaseModel):
    text: str

class STTService:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def transcribe(self, file_path: str) -> STTResult:
        url = 'https://mohir.ai/api/v1/stt'
        headers = {
            "Authorization": self.api_key
        }
        files = {
            "file": ("audio_temp.wav", open(file_path, "rb")),
        }
        data = {
            "return_offsets": "true",
            "run_diarization": "false",
            "language": "uz",
            "blocking": "true",
        }

        try:
            response = requests.post(url, headers=headers, files=files, data=data)
            if response.status_code == 200:
                result = response.json()
                return STTResult(text=result.get("text", ""))
            else:
                return STTResult(text=f"Request failed with status code {response.status_code}: {response.text}")
        except requests.exceptions.Timeout:
            return STTResult(text="Request timed out. The API response took too long to arrive.")
