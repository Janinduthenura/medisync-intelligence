from pydantic import BaseModel

class TranscriptionOutput(BaseModel):
    transcript: str                  # make sure this matches
    duration_seconds: float
    model_used: str