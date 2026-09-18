"""골든셋 평가: 핵심 필드 추출 정확도, 출처 Top-3 매칭률, 충돌 Recall"""
import asyncio, json
from pathlib import Path
from app.pipeline import understand, extract, normalize, search, verify

GOLDEN = Path(__file__).parent / "golden"
CORE = ("title", "organization", "apply_period", "benefit_amount", "target")


async def evaluate(case: dict) -> dict:
    u = await understand.run(case["input"]["text"], case["input"].get("images", []))
    ex = await normalize.run(await extract.run(u))
    sources = await search.run(ex)
    ver = await verify.run(ex, sources)
    exp = case["expected"]
    field_hits = sum(1 for f in CORE if str(getattr(ex, f, None)) == str(exp["fields"].get(f)))
    source_hit = any(s.url == exp["official_url"] for s in sources)
    conflicts = {f.field for f in ver.fields if f.status == "CONFLICT"}
    conflict_recall = (len(conflicts & set(exp["conflict_fields"])) / len(exp["conflict_fields"])) if exp["conflict_fields"] else None
    return {"id": case["id"], "field_acc": field_hits / len(CORE), "source_top3": source_hit, "conflict_recall": conflict_recall}


async def main():
    cases = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(GOLDEN.glob("*.json")) if not p.name.startswith("_")]
    results = [await evaluate(c) for c in cases]
    n = len(results) or 1
    print(f"cases={len(results)}")
    print(f"field_acc={sum(r['field_acc'] for r in results)/n:.2%}  (목표 85%)")
    print(f"source_top3={sum(r['source_top3'] for r in results)/n:.2%}  (목표 80%)")
    cr = [r["conflict_recall"] for r in results if r["conflict_recall"] is not None]
    print(f"conflict_recall={(sum(cr)/len(cr) if cr else 0):.2%}  (목표 80%)")


if __name__ == "__main__":
    asyncio.run(main())
