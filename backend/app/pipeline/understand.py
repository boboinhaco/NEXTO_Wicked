# A1: 이미지+텍스트 멀티모달 이해 (TODO: LLM 호출)
async def run(text: str, image_paths: list[str]) -> dict:
    return {"text": text, "image_count": len(image_paths), "summary": text[:300]}
