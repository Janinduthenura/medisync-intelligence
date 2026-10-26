import time
import httpx
from schemas.models import DrugCheck, DrugValidationOutput

OPENFDA_URL = "https://api.fda.gov/drug/label.json"


def _pick_generic_name(name: str, results: list) -> str | None:
    """Pick the best generic name from the OpenFDA results, avoiding combination drugs."""
    all_names = [
        g.lower()
        for r in results
        for g in r.get("openfda", {}).get("generic_name", [])
    ]

    # Single-ingredient names only (combination products contain " and " or a comma)
    single = [g for g in all_names if " and " not in g and "," not in g]

    # 1. A single-ingredient name that matches or starts with the drug name
    #    (e.g. "metformin" -> "metformin hydrochloride")
    for g in single:
        if g == name.lower() or g.startswith(name.lower()):
            return g

    # 2. Otherwise the first single-ingredient name (e.g. "Tylenol" -> "acetaminophen")
    if single:
        return single[0]

    # 3. Only combination products were found, so don't guess
    return None


def _check_drug(name: str) -> DrugCheck:
    query = f'openfda.generic_name:"{name}" OR openfda.brand_name:"{name}"'
    try:
        response = httpx.get(
            OPENFDA_URL,
            params={"search": query, "limit": 10},
            timeout=10
        )
    except httpx.HTTPError:
        return DrugCheck(name=name, status="UNVERIFIED")

    if response.status_code == 404:          # OpenFDA's way of saying "no matches"
        return DrugCheck(name=name, status="FLAGGED")
    if response.status_code != 200:          # rate limit, server error, etc.
        return DrugCheck(name=name, status="UNVERIFIED")

    results = response.json().get("results", [])
    generic = _pick_generic_name(name, results)
    return DrugCheck(name=name, status="VALIDATED", generic_name=generic)


def validate_drugs(drugs: list[str]) -> DrugValidationOutput:
    start = time.time()
    unique = list(dict.fromkeys(d.strip() for d in drugs if d.strip()))
    checks = [_check_drug(d) for d in unique]

    return DrugValidationOutput(
        validated_drugs=[c.name for c in checks if c.status == "VALIDATED"],
        flagged_drugs=[c.name for c in checks if c.status == "FLAGGED"],
        unverified_drugs=[c.name for c in checks if c.status == "UNVERIFIED"],
        checks=checks,
        duration_seconds=round(time.time() - start, 2)
    )