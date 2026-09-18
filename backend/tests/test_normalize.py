from datetime import date
from app.pipeline.normalize import parse_amount, resolve_relative_end
from app.pipeline.verify import compare_period, compare_age


def test_parse_amount():
    assert parse_amount("최대 20만원") == 200_000
    assert parse_amount("1,500,000원") == 1_500_000


def test_relative_end_is_ambiguous():
    d, status = resolve_relative_end("9월까지", today=date(2026, 9, 19))
    assert d == "2026-09-30" and status == "ambiguous"


def test_period_refined_and_conflict():
    assert compare_period({"start": "2026-09-01", "end": "2026-09-15"}, {"start": "2026-09-01", "end": "2026-09-30"}) == "REFINED"
    assert compare_period({"start": "2026-10-01", "end": "2026-10-15"}, {"start": "2026-09-01", "end": "2026-09-30"}) == "CONFLICT"


def test_age_conflict():
    assert compare_age({"age_min": 19, "age_max": 34}, {"age_min": 19, "age_max": 39}) == "REFINED"
    assert compare_age({"age_min": 19, "age_max": 45}, {"age_min": 19, "age_max": 39}) == "CONFLICT"
