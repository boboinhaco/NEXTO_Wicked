from datetime import datetime, timedelta, timezone
from fastapi import Depends, Header
from jose import jwt, JWTError
from .config import settings
from .errors import NextoError

DEMO_USER_ID = "00000000-0000-0000-0000-000000000001"


# 데모 세션용 JWT 발급
def create_token(user_id: str) -> str:
    payload = {"sub": user_id, "exp": datetime.now(timezone.utc) + timedelta(hours=12)}
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


# Authorization 헤더에서 user_id 추출, 없으면 데모 사용자
def current_user(authorization: str | None = Header(default=None)) -> str:
    if not authorization:
        return DEMO_USER_ID
    try:
        return jwt.decode(authorization.removeprefix("Bearer "), settings.jwt_secret, algorithms=["HS256"])["sub"]
    except JWTError:
        raise NextoError("UNAUTHORIZED", "세션이 만료됐어요.", status=401)
