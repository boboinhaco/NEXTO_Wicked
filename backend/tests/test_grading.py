from app.schemas import FieldResult
from app.services.grading import grade


def _f(field, status): return FieldResult(field=field, status=status)


def test_unverified_without_source():
    assert grade(False, [_f("title", "VERIFIED")]) == "UNVERIFIED"


def test_high_requires_three_grounded_and_no_conflict():
    fields = [_f("title", "VERIFIED"), _f("apply_period", "REFINED"), _f("benefit_amount", "VERIFIED"), _f("target", "ADDED")]
    assert grade(True, fields) == "HIGH"


def test_review_on_conflict():
    fields = [_f("title", "VERIFIED"), _f("apply_period", "VERIFIED"), _f("benefit_amount", "VERIFIED"), _f("target", "CONFLICT")]
    assert grade(True, fields) == "REVIEW"
