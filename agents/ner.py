import time
from transformers import pipeline
from schemas.models import ExtractedEntity, NEROutput

print("Loading biomedical NER model...")
ner_pipeline = pipeline(
    "token-classification",
    model="d4data/biomedical-ner-all",
    aggregation_strategy="simple"
)
print("NER model ready.")

print("Loading urgency classifier...")
urgency_classifier = pipeline(
    "zero-shot-classification",
    model="typeform/distilbert-base-uncased-mnli"
)
print("Urgency classifier ready.")

URGENCY_LABELS = [
    "routine medical visit",
    "urgent medical attention",
    "emergency medical situation"
]

URGENCY_LABEL_MAP = {
    "Sign_symptom": "SYMPTOM",
    "Medication": "DRUG",
    "Dosage": "DOSAGE",
    "Disease_disorder": "CONDITION",
    "Therapeutic_procedure": "PROCEDURE",
    "Diagnostic_procedure": "PROCEDURE",
    "Biological_structure": "ANATOMY",  # not in your original 5, but genuinely distinct info worth keeping
}

def extract_entities(transcript: str) -> NEROutput:
    start = time.time()

    raw_entities = ner_pipeline(transcript)
    entities = [
        ExtractedEntity(
            text=e["word"],
            label=LABEL_MAP.get(e["entity_group"], e["entity_group"]),
            confidence=float(e["score"])
        )
        for e in raw_entities
    ]

    # Step 2: classify urgency
    urgency_result = urgency_classifier(transcript, candidate_labels=URGENCY_LABELS)
    top_label = urgency_result["labels"][0]
    top_score = urgency_result["scores"][0]

    elapsed = round(time.time() - start, 2)

    return NEROutput(
        entities=entities,
        urgency=URGENCY_LABEL_MAP[top_label],
        urgency_confidence=round(float(top_score), 2),
        duration_seconds=elapsed
    )