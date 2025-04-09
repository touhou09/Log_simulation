import asyncio
from collections import defaultdict

stream_queues = defaultdict(list)  # 서비스별 큐
all_stream_queues = []  # 전체 로그 수신 구독자 목록

def register_stream_queue(service: str = None):
    q = asyncio.Queue()
    if service:
        stream_queues[service].append(q)
    else:
        all_stream_queues.append(q)
    return q

async def publish_to_streams(service: str, message: str):
    for q in stream_queues.get(service, []):
        await q.put(message)
    for q in all_stream_queues:
        await q.put(message)