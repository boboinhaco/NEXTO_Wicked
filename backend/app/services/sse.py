import asyncio
from collections import defaultdict

# job_id → 구독 큐 목록
_subscribers: dict[str, list[asyncio.Queue]] = defaultdict(list)


def subscribe(job_id: str) -> asyncio.Queue:
    q: asyncio.Queue = asyncio.Queue()
    _subscribers[job_id].append(q)
    return q


def unsubscribe(job_id: str, q: asyncio.Queue):
    _subscribers[job_id].remove(q)


# event: progress | completed | failed
async def publish(job_id: str, event: str, data: dict):
    for q in list(_subscribers.get(job_id, [])):
        await q.put({"event": event, "data": data})
