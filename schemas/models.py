from pydantic import BaseModel

class TranscriptionOutput(BaseModel):
    text: str                  # make sure this matches
    duration_seconds: float
    model_used: str 

class SummarizeRequest(BaseModel):
    text: str

class SOAPNoteOutput(BaseModel):
    soap_note: str
    duration_seconds: float
    model_used: str

class PipelineOutput(BaseModel):
    transcript: str
    soap_note: str
    transcription_seconds: float
    summarization_seconds: float