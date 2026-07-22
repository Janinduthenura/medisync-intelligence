import time
from transformers import pipeline
from schemas.models import SOAPNoteOutput

print("Loading FLAN-T5 summarizer...")
summarizer = pipeline(
    "text2text-generation",
    model="google/flan-t5-large",
    max_length=150
)
print("FLAN-T5 ready.")

SECTION_PROMPTS = {
    "subjective": "From this doctor-patient conversation, extract only what the patient reports: symptoms, complaints, and history. Conversation: {transcript}",
    "objective": "From this doctor-patient conversation, extract only measurable findings such as vitals or medications mentioned. If none are mentioned, say 'None mentioned'. Conversation: {transcript}",
    "assessment": "From this doctor-patient conversation, state the likely diagnosis or clinical impression given by the doctor. Conversation: {transcript}",
    "plan": "From this doctor-patient conversation, list only the medications, dosages, or instructions that are explicitly mentioned in the conversation. Do not guess or infer medication names that are not stated. If no specific medication is named, say 'Prescription given, medication not specified in conversation'. Conversation: {transcript}",
}

def _extract_section(transcript: str, prompt_template: str) -> str:
    prompt = prompt_template.format(transcript=transcript)
    result = summarizer(prompt, truncation=True)
    return result[0]["generated_text"].strip()

def summarize_to_soap(transcript: str) -> SOAPNoteOutput:
    start = time.time()

    subjective = _extract_section(transcript, SECTION_PROMPTS["subjective"])
    objective = _extract_section(transcript, SECTION_PROMPTS["objective"])
    assessment = _extract_section(transcript, SECTION_PROMPTS["assessment"])
    plan = _extract_section(transcript, SECTION_PROMPTS["plan"])

    soap_note = (
        f"S: {subjective}\n"
        f"O: {objective}\n"
        f"A: {assessment}\n"
        f"P: {plan}"
    )

    elapsed = round(time.time() - start, 2)

    return SOAPNoteOutput(
        soap_note=soap_note,
        duration_seconds=elapsed,
        model_used="google/flan-t5-large"
    )