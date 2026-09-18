import hashlib
from pathlib import Path
from io import BytesIO
from fastapi import UploadFile
from PIL import Image
from ..core.config import settings
from ..core.errors import NextoError

ALLOWED = {"image/jpeg", "image/png", "image/webp"}
MAX_BYTES = 8 * 1024 * 1024


# 5.1 입력 제약: MIME 검사, decode 확인, 장변 1600px 리사이즈 후 저장
async def save_image(file: UploadFile, share_id: str, order: int) -> str:
    if file.content_type not in ALLOWED: raise NextoError("INVALID_FILE", "JPG/PNG/WEBP만 올릴 수 있어요.")
    raw = await file.read()
    if len(raw) > MAX_BYTES: raise NextoError("INVALID_FILE", "이미지는 장당 8MB 이하여야 해요.")
    try:
        img = Image.open(BytesIO(raw)); img.verify(); img = Image.open(BytesIO(raw)).convert("RGB")
    except Exception:
        raise NextoError("INVALID_FILE", "이미지를 읽을 수 없어요.")
    img.thumbnail((1600, 1600))
    out_dir = Path(settings.storage_dir) / share_id; out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{order}.jpg"; img.save(path, "JPEG", quality=88)
    return str(path)


# 5.1 중복 방지: 입력 해시
def input_hash(text: str, image_bytes_list: list[bytes]) -> str:
    h = hashlib.sha256(text.encode())
    for b in image_bytes_list: h.update(hashlib.sha256(b).digest())
    return h.hexdigest()
