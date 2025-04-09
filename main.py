from fastapi import FastAPI
from api import stream, simulate
from generator import start_log_generator
import asyncio

app = FastAPI()

app.include_router(stream.router)
app.include_router(simulate.router)

@app.on_event("startup")
async def start_generator():
    class NoOpOutput:
        async def write(self, message: str, topic: str):
            pass  # 출력 없음
    asyncio.create_task(start_log_generator(NoOpOutput()))
