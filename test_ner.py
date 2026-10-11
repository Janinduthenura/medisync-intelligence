from agents.ner import extract_entities

result = extract_entities(
    "Patient reports chest pain and shortness of breath. "
    "Currently taking metformin 500mg twice daily."
)

print("Urgency:", result.urgency, result.urgency_confidence)
for e in result.entities:
    print(e.label, "->", e.text)