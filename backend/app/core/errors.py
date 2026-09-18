from fastapi import Request
from fastapi.responses import JSONResponse


# 명세서 9.1 공통 오류 계약
class NextoError(Exception):
    def __init__(self, code: str, message: str, stage: str | None = None, retryable: bool = False, status: int = 400):
        self.code, self.message, self.stage, self.retryable, self.status = code, message, stage, retryable, status

    def to_dict(self):
        return {"code": self.code, "stage": self.stage, "message": self.message, "retryable": self.retryable}


async def nexto_error_handler(_: Request, exc: NextoError):
    return JSONResponse(status_code=exc.status, content={"success": False, "data": None, "error": exc.to_dict()})


async def generic_error_handler(_: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"success": False, "data": None, "error": {"code": "INTERNAL", "message": str(exc), "retryable": True}})


# 성공 envelope
def ok(data):
    return {"success": True, "data": data, "error": None}
