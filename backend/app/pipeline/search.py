import hashlib
from urllib.parse import urlparse
from ..schemas import ExtractionPayload, SourceDoc

# 명세서 7.1 도메인 화이트리스트
PUBLIC = ("lh.or.kr", "i-sh.co.kr", "applyhome.co.kr")
FINANCE = ("kinfa.or.kr", "fsc.go.kr")
SECONDARY = ("news", "blog.naver.com")


def classify_domain(url: str) -> str:
    host = urlparse(url).netloc
    if any(host.endswith(d) for d in PUBLIC): return "OFFICIAL_PUBLIC"
    if any(host.endswith(d) for d in FINANCE): return "OFFICIAL_FINANCE"
    if host.endswith(".go.kr"): return "OFFICIAL_GOV"
    if any(s in host for s in SECONDARY): return "SECONDARY"
    return "UNKNOWN"


def url_hash(url: str) -> str:
    return hashlib.sha256(url.split("#")[0].rstrip("/").encode()).hexdigest()


# 검색 질의 생성: 사업명/기관/연도 (TODO: LLM 보조)
def build_queries(ex: ExtractionPayload) -> list[str]:
    parts = [ex.title, ex.organization or "", "2026"]
    return [" ".join(p for p in parts if p), f"{ex.title} 공고"]


# 순위: 공식 도메인 우선
RANK = {"OFFICIAL_GOV": 0, "OFFICIAL_PUBLIC": 1, "OFFICIAL_FINANCE": 2, "SECONDARY": 3, "UNKNOWN": 4}


# A3: 검색 API → 화이트리스트 정렬 → 본문 확보 → Top 3 (TODO: 검색 API/본문 fetch)
async def run(ex: ExtractionPayload) -> list[SourceDoc]:
    candidates: list[SourceDoc] = []
    for s in candidates: s.domain_type = classify_domain(s.url)
    candidates.sort(key=lambda s: RANK[s.domain_type])
    for i, s in enumerate(candidates[:3]): s.rank = i
    return candidates[:3]
