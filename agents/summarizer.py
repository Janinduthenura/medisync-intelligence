import time
from concurrent.futures import ThreadPoolExecutor
from transformers import pipeline
from schemas.models import SOAPNoteOutput, SOAPSections

print("Loading FLAN-T5 summarizer...")
summarizer = pipeline(
    "text2text-generation",
    model="google/flan-t5-large",
    max_length=150
)
print("FLAN-T5 ready.")

SECTION_PROMPTS = {
    "subjective": "From this doctor-patient conversation, extract only what the patient reports: symptoms, complaints, and history. If not mentioned, say 'Not specified'. Conversation: {transcript}",
    "objective": "From this doctor-patient conversation, extract only measurable findings such as vitals or medications mentioned. If none are mentioned, say 'None mentioned'. Conversation: {transcript}",
    "assessment": "From this doctor-patient conversation, state the likely diagnosis or clinical impression given by the doctor. If not stated, say 'Not specified'. Conversation: {transcript}",
    "plan": "From this doctor-patient conversation, list only the medications, dosages, or instructions explicitly mentioned. Do not guess or infer medication names not stated. If no specific medication is named, say 'Prescription given, medication not specified in conversation'. Conversation: {transcript}",
}

def _extract_section(transcript: str, prompt_template: str) -> str:
    prompt = prompt_template.format(transcript=transcript)
    result = summarizer(prompt, truncation=True)
    return result[0]["generated_text"].strip()

def summarize_to_soap(transcript: str) -> SOAPNoteOutput:
    start = time.time()

    if len(transcript.strip()) < 20:
        raise ValueError(
            f"Transcript too short to summarize: '{transcript.strip()}'"
        )

    # Run all 4 sections in parallel instead of sequentially
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            section: executor.submit(_extract_section, transcript, prompt)
            for section, prompt in SECTION_PROMPTS.items()
        }
        results = {section: future.result() for section, future in futures.items()}

    soap_note = (
        f"S: {results['subjective']}\n"
        f"O: {results['objective']}\n"
        f"A: {results['assessment']}\n"
        f"P: {results['plan']}"
    )

    elapsed = round(time.time() - start, 2)

    return SOAPNoteOutput(
    soap_note=soap_note,
    sections=SOAPSections(
        subjective=results["subjective"],
        objective=results["objective"],
        assessment=results["assessment"],
        plan=results["plan"]
    ),
    duration_seconds=elapsed,
    model_used="google/flan-t5-large"
    )