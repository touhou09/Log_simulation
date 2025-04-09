from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from stream_queue import register_stream_queue
import asyncio

router = APIRouter()

@router.get("/stream/{service}")
async def stream_logs(service: str):
    q = register_stream_queue(service)

    async def event_generator():
        try:
            while True:
                msg = await q.get()
                yield msg + "\n"
        except asyncio.CancelledError:
            pass

    return StreamingResponse(event_generator(), media_type="text/plain")

@router.get("/stream")
async def stream_all():
    q = register_stream_queue()  # 서비스 이름 없이 전체 등록

    async def event_generator():
        try:
            while True:
                msg = await q.get()
                yield msg + "\n"
        except asyncio.CancelledError:
            pass

    return StreamingResponse(event_generator(), media_type="text/plain")