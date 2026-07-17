import time
from transformers import pipeline
from schemas.models import TranscriptionOutput
import librosa

print("Loading Whisper model...")
asr = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-base",
    chunk_length_s=30,
    stride_length_s=5,
    return_timestamps=False
)
print("Whisper ready.")

def transcribe_audio(audio_path: str) -> TranscriptionOutput:
    start = time.time()
    audio, sr = librosa.load(audio_path, sr=16000)
    result = asr({"array": audio, "sampling_rate": sr})
    elapsed = time.time() - start

    return TranscriptionOutput(
        text=result["text"],
        model_used="openai/whisper-base",
        duration_seconds=elapsed
    )