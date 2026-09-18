from fastapi import APIRouter
from ..core.security import create_token, DEMO_USER_ID
from ..core.errors import ok

router = APIRouter(prefix="/api/auth", tags=["auth"])


# 데모 세션 발급
@router.post("/demo")
async def demo_session():
    return ok({"token": create_token(DEMO_USER_ID), "user_id": DEMO_USER_ID})
