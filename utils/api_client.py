import requests
from config import API_BASE_URL

def check_health() -> dict:
    response = requests.get(f"{API_BASE_URL}/health")
    response.raise_for_status()
    return response.json()

def run_pipeline(audio_bytes: bytes, filename: str) -> dict:
    files = {"file": (filename, audio_bytes, "audio/mpeg")}
    response = requests.post(
        f"{API_BASE_URL}/pipeline",
        files=files,
        timeout=120
    )
    response.raise_for_status()
    return response.json()