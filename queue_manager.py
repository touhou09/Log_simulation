import asyncio
from config import QUEUE_MAXSIZE

log_queue = asyncio.Queue(maxsize=QUEUE_MAXSIZE)