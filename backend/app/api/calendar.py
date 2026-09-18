from datetime import date, datetime, time, timezone
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.session import get_db
from ..db.models import CalendarEvent, SavedItem
from ..core.security import current_user
from ..core.errors import ok

router = APIRouter(prefix="/api/calendar", tags=["calendar"])


# 기간별 이벤트 + 항목 제목
@router.get("")
async def range_events(from_: date = Query(alias="from"), to: date = Query(), user_id: str = Depends(current_user), db: AsyncSession = Depends(get_db)):
    start = datetime.combine(from_, time.min, tzinfo=timezone.utc); end = datetime.combine(to, time.max, tzinfo=timezone.utc)
    rows = (await db.execute(select(CalendarEvent, SavedItem).join(SavedItem, SavedItem.item_id == CalendarEvent.item_id)
                             .where(SavedItem.user_id == user_id, CalendarEvent.start_at.between(start, end)).order_by(CalendarEvent.start_at))).all()
    return ok([{"event_id": str(e.event_id), "item_id": str(i.item_id), "title": i.title, "category": i.category, "event_type": e.event_type,
                "start_at": e.start_at.isoformat(), "end_at": e.end_at.isoformat() if e.end_at else None, "date_status": e.date_status} for e, i in rows])
