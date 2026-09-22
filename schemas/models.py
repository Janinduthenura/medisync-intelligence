from pydantic import BaseModel
from typing import Optional
from typing import List

class ExtractedEntity(BaseModel):
    text: str
    label: str
    confidence: float

class NEROutput(BaseModel):
    entities: List[ExtractedEntity]
    urgency: str
    urgency_confidence: float
    duration_seconds: float

class SOAPSections(BaseModel):
    subjective: str
    objective: str
    assessment: str
    plan: str

class SOAPNoteOutput(BaseModel):
    soap_note: str           # full formatted string — for display
    sections: SOAPSections   # individual parts — for eval
    duration_seconds: float
    model_used: str

class TranscriptionOutput(BaseModel):
    text: str                  # make sure this matches
    duration_seconds: float
    model_used: str 

class SummarizeRequest(BaseModel):
    text: str

class PipelineOutput(BaseModel):
    transcript: str
    soap_note: str
    sections: SOAPSections
    transcription_seconds: float
    summarization_seconds: float