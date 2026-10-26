from agents.drug_validator import validate_drugs

result = validate_drugs(["metformin", "Tylenol", "metphormin", "xyzabc"])
print("Validated:", result.validated_drugs)
print("Flagged:", result.flagged_drugs)
print("Unverified:", result.unverified_drugs)
for c in result.checks:
    print(c.name, "->", c.status, c.generic_name)