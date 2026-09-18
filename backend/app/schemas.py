from typing import Literal, Optional
from pydantic import BaseModel

Category = Literal["POLICY_HOUSING", "POLICY_JOB", "POLICY_LIVING", "SUBSCRIPTION", "FINANCE", "EVENT", "RECRUIT", "CONTEST", "OTHER"]
FieldStatus = Literal["VERIFIED", "REFINED", "CONFLICT", "ADDED", "AMBIGUOUS", "UNVERIFIED"]
Grade = Literal["HIGH", "REVIEW", "UNVERIFIED"]
DomainType = Literal["OFFICIAL_GOV", "OFFICIAL_PUBLIC", "OFFICIAL_FINANCE", "SECONDARY", "UNKNOWN"]
Stage = Literal["UNDERSTAND", "EXTRACT", "NORMALIZE", "SEARCH", "VERIFY", "DONE"]


class Period(BaseModel):
    start: Optional[str] = None
    end: Optional[str] = None
    status: Literal["exact", "ambiguous", "unknown"] = "unknown"


# FR-03 구조화 추출 결과
class ExtractionPayload(BaseModel):
    title: str
    category: Category = "OTHER"
    organization: Optional[str] = None
    benefit_amount: Optional[dict] = None
    target: Optional[dict] = None
    apply_period: Period = Period()
    event_period: Optional[Period] = None
    location: Optional[dict] = None
    requirements: list[str] = []
    raw_evidence: list[str] = []


class SourceDoc(BaseModel):
    url: str
    domain_type: DomainType = "UNKNOWN"
    title: str = ""
    published_at: Optional[str] = None
    excerpt: str = ""
    rank: int = 0


class FieldResult(BaseModel):
    field: str
    sns_value: Optional[object] = None
    official_value: Optional[object] = None
    status: FieldStatus
    evidence: Optional[str] = None


# FR-05 검증 결과, 숫자 confidence 없음
class VerificationPayload(BaseModel):
    primary_source: Optional[SourceDoc] = None
    fields: list[FieldResult] = []
    overall_grade: Grade = "UNVERIFIED"


class CreateItemRequest(BaseModel):
    share_id: str
    extraction_id: str
    title: str
    category: Category = "OTHER"
    fields: dict
    user_overrides: list[str] = []
    primary_source_id: Optional[str] = None


class UpdateItemRequest(BaseModel):
    title: Optional[str] = None
    fields: Optional[dict] = None
    status: Optional[str] = None
