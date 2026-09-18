import re
from datetime import date
from ..schemas import ExtractionPayload

# 금액 문자열 → 원 단위 정수
def parse_amount(text: str | None) -> int | None:
    if not text: return None
    m = re.search(r"(\d[\d,]*)\s*(만|억)?\s*원?", text)
    if not m: return None
    n = int(m.group(1).replace(",", ""))
    return n * {"만": 10_000, "억": 100_000_000}.get(m.group(2), 1)


# "9월까지" 같은 상대 표현을 후보 날짜로, 확정은 사용자 확인
def resolve_relative_end(text: str, today: date | None = None) -> tuple[str | None, str]:
    today = today or date.today()
    m = re.search(r"(\d{1,2})월\s*까지", text)
    if m:
        month = int(m.group(1)); year = today.year if month >= today.month else today.year + 1
        import calendar
        return f"{year}-{month:02d}-{calendar.monthrange(year, month)[1]}", "ambiguous"
    return None, "unknown"


# A5: 규칙 우선 정규화
async def run(ex: ExtractionPayload) -> ExtractionPayload:
    if ex.benefit_amount and "text" in ex.benefit_amount and "value" not in ex.benefit_amount:
        ex.benefit_amount["value"] = parse_amount(ex.benefit_amount["text"])
    return ex
