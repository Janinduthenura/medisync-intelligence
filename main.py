import os
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException
from agents.transcription import transcribe_audio
from agents.summarizer import summarize_to_soap
from schemas.models import (
    TranscriptionOutput,
    SummarizeRequest,
    SOAPNoteOutput,
    PipelineOutput
)

app = FastAPI(
    title="MediSync Intelligence",
    description="Multi-agent clinical note assistant",
    version="0.1.0"
)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "whisper": "loaded",
        "bart": "loaded"
    }

@app.post("/transcribe", response_model=TranscriptionOutput)
async def transcribe(file: UploadFile = File(...)):
    if not file.filename.endswith((".mp3", ".wav", ".m4a")):
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Use .mp3, .wav or .m4a"
        )

    # Save uploaded file to a temp location
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=os.path.splitext(file.filename)[1]
    ) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        result = transcribe_audio(tmp_path)
    finally:
        os.remove(tmp_path)   # always clean up

    return result

@app.post("/summarize", response_model=SOAPNoteOutput)
def summarize(request: SummarizeRequest):
    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Transcript text cannot be empty"
        )
    return summarize_to_soap(request.text)

@app.post("/pipeline", response_model=PipelineOutput)
async def full_pipeline(file: UploadFile = File(...)):
    # Step 1: transcribe
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=os.path.splitext(file.filename)[1]
    ) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        transcription = transcribe_audio(tmp_path)
    finally:
        os.remove(tmp_path)

    # Step 2: summarize
    soap = summarize_to_soap(transcription.text)

    return PipelineOutput(
        transcript=transcription.text,
        soap_note=soap.soap_note,
        transcription_seconds=transcription.duration_seconds,
        summarization_seconds=soap.duration_seconds
    )