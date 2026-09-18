from ..schemas import ExtractionPayload, SourceDoc, VerificationPayload, FieldResult
from ..services.grading import grade

CORE_FIELDS = ("title", "apply_period", "benefit_amount", "target")


# 기간 룰 비교: SNS ⊂ 공식 → REFINED, 교집합 없음 → CONFLICT
def compare_period(sns: dict, official: dict) -> str:
    if not sns.get("end") or not official.get("end"): return "AMBIGUOUS"
    if sns == official: return "VERIFIED"
    if official.get("start", "") <= sns.get("start", official.get("start", "")) and sns["end"] <= official["end"]: return "REFINED"
    return "CONFLICT"


# 연령 구간 비교
def compare_age(sns: dict, official: dict) -> str:
    keys = ("age_min", "age_max")
    if any(sns.get(k) is None or official.get(k) is None for k in keys): return "AMBIGUOUS"
    if all(sns[k] == official[k] for k in keys): return "VERIFIED"
    if official["age_min"] <= sns["age_min"] and sns["age_max"] <= official["age_max"]: return "REFINED"
    return "CONFLICT"


# A4: 룰 + LLM 근거 판정 (TODO: 자유텍스트 필드 LLM 비교)
async def run(ex: ExtractionPayload, sources: list[SourceDoc]) -> VerificationPayload:
    if not sources:
        fields = [FieldResult(field=f, sns_value=getattr(ex, f, None), status="UNVERIFIED") for f in CORE_FIELDS]
        return VerificationPayload(fields=fields, overall_grade="UNVERIFIED")
    fields: list[FieldResult] = []
    # TODO: sources[0].excerpt에서 공식값 추출 후 compare_* 적용
    return VerificationPayload(primary_source=sources[0], fields=fields, overall_grade=grade(True, fields))
