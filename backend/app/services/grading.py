from ..schemas import FieldResult

CORE = {"title", "apply_period", "benefit_amount", "target"}


# 명세서 6.3: HIGH / REVIEW / UNVERIFIED 3단계
def grade(has_official_source: bool, fields: list[FieldResult]) -> str:
    if not has_official_source: return "UNVERIFIED"
    statuses = {f.field: f.status for f in fields}
    grounded = sum(1 for f in CORE if statuses.get(f) in ("VERIFIED", "REFINED", "ADDED"))
    has_issue = any(s in ("CONFLICT", "AMBIGUOUS") for s in statuses.values())
    return "HIGH" if grounded >= 3 and not has_issue else "REVIEW"
