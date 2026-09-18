from ..schemas import ExtractionPayload


# A2: JSON Schema 강제 추출 (TODO: structured output LLM 호출)
async def run(understanding: dict) -> ExtractionPayload:
    return ExtractionPayload(title="(추출 미구현)", raw_evidence=[understanding.get("summary", "")])
