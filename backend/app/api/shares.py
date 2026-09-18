from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.session import get_db
from ..db.models import ContentShare, MediaAsset, AnalysisJob, Extraction, SourceDocument, VerificationResult
from ..core.security import current_user
from ..core.errors import NextoError, ok
from ..services import storage
from ..services.job_runner import run_job

router = APIRouter(prefix="/api/shares", tags=["shares"])


# FR-01: 업로드 + job 생성, 10분 내 동일 입력은 기존 job 재사용
@router.post("")
async def create_share(bg: BackgroundTasks, images: list[UploadFile] = File(default=[]), text: str = Form(default=""),
                       original_url: str = Form(default=""), user_id: str = Depends(current_user), db: AsyncSession = Depends(get_db)):
    if not images and not text.strip(): raise NextoError("LOW_TEXT_CONTENT", "이미지나 텍스트 중 하나는 필요해요.")
    if len(images) > 5: raise NextoError("INVALID_FILE", "이미지는 최대 5장이에요.")
    if len(text) > 3000: raise NextoError("INVALID_FILE", "텍스트는 3,000자 이하로 넣어주세요.")
    blobs = [await f.read() for f in images]
    for f in images: await f.seek(0)
    h = storage.input_hash(text, blobs)
    recent = (await db.execute(select(ContentShare).where(ContentShare.input_hash == h, ContentShare.created_at > datetime.now(timezone.utc) - timedelta(minutes=10)))).scalar_one_or_none()
    if recent:
        job = (await db.execute(select(AnalysisJob).where(AnalysisJob.share_id == recent.share_id).order_by(AnalysisJob.started_at.desc()))).scalars().first()
        if job: return ok({"share_id": str(recent.share_id), "job_id": str(job.job_id), "status": job.status, "reused": True})
    share = ContentShare(user_id=user_id, text=text, original_url=original_url or None, input_hash=h)
    db.add(share); await db.flush()
    for i, f in enumerate(images):
        db.add(MediaAsset(share_id=share.share_id, storage_key=await storage.save_image(f, str(share.share_id), i), asset_order=i))
    job = AnalysisJob(share_id=share.share_id, status="QUEUED", stage_results={})
    db.add(job); await db.commit()
    bg.add_task(run_job, str(job.job_id))
    return ok({"share_id": str(share.share_id), "job_id": str(job.job_id), "status": "QUEUED"})


# 검토 화면용 통합 조회: 추출 + 출처 + 검증
@router.get("/{share_id}/result")
async def get_result(share_id: str, db: AsyncSession = Depends(get_db)):
    ex = (await db.execute(select(Extraction).where(Extraction.share_id == share_id).order_by(Extraction.created_at.desc()))).scalars().first()
    if not ex: raise NextoError("NOT_FOUND", "분석 결과가 아직 없어요.", status=404)
    sources = (await db.execute(select(SourceDocument).where(SourceDocument.extraction_id == ex.extraction_id).order_by(SourceDocument.rank))).scalars().all()
    ver = (await db.execute(select(VerificationResult).where(VerificationResult.extraction_id == ex.extraction_id).order_by(VerificationResult.verified_at.desc()))).scalars().first()
    return ok({
        "share_id": share_id,
        "extraction": {"extraction_id": str(ex.extraction_id), "model_name": ex.model_name, "schema_version": ex.schema_version, **ex.payload_json},
        "sources": [{"source_id": str(s.source_id), "url": s.url, "domain_type": s.domain_type, "title": s.title, "excerpt": s.excerpt, "rank": s.rank} for s in sources],
        "verification": {"fields": ver.fields_json, "overall_grade": ver.overall_grade, "verified_at": ver.verified_at.isoformat()} if ver else None,
    })
