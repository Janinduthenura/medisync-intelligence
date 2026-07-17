import time
from transformers import pipeline
from schemas.models import SOAPNoteOutput

print("Loading BART summarizer...")
summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn",
    max_length=256,
    min_length=60,
    do_sample=False
)
print("BART ready.")

SOAP_PROMPT = """
Convert this doctor-patient conversation transcript into a SOAP note.

S (Subjective): What the patient reports — symptoms, complaints, history.
O (Objective): Measurable findings — vitals, medications mentioned.
A (Assessment): Likely diagnosis or clinical impression.
P (Plan): Next steps — tests, medications, follow-up.

Transcript:
{transcript}

SOAP Note:
"""

def summarize_to_soap(transcript: str) -> SOAPNoteOutput:
    start = time.time()

    result = summarizer(transcript, truncation=True)
    soap_note = result[0]["summary_text"].strip()

    elapsed = round(time.time() - start, 2)

    return SOAPNoteOutput(
        soap_note=soap_note,
        duration_seconds=elapsed,
        model_used="facebook/bart-large-cnn"
    )