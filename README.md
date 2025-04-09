# FastAPI 로그 시뮬레이터

FastAPI 기반으로 제작된 경량 로그 시뮬레이터입니다. 여러 서비스의 로그를 실시간으로 생성하고 `/stream` API를 통해 외부에서 구독할 수 있도록 설계되었습니다. Kafka, Redis 등 메시지 큐에 연결해 테스트하거나, 관측/모니터링 시스템과 통합하기에 적합합니다.

---

## 🚀 주요 기능

- `member`, `order`, `payment` 등 다중 서비스 로그 시뮬레이션
- `/stream` 및 `/stream/{service}` 를 통한 실시간 로그 스트리밍
- 시뮬레이터 모듈만 추가하면 새로운 서비스 확장 가능
- 외부 메시지 큐(Kafka, Redis 등)와 쉽게 연동 가능
- `/simulate/{service}` API로 수동 테스트 가능

---

## 📁 프로젝트 구조

```
log_simulation/
├── main.py                  # FastAPI 진입점
├── generator.py            # 로그 생성 루프
├── stream_queue.py         # 서비스별 내부 큐 관리
├── queue_manager.py        # (선택적) 내부 큐 예시
├── api/
│   ├── stream.py           # /stream API
│   └── simulate.py         # /simulate API
├── simulator/
│   ├── member.py
│   ├── order.py
│   └── payment.py
```

---

## 🔌 스트리밍 API

### 전체 로그 구독

```bash
GET /stream
```

### 특정 서비스 로그 구독

```bash
GET /stream/member
GET /stream/order
GET /stream/payment
```

> 응답 형식: Server-Sent Streaming (text/plain) 각 줄마다 JSON 로그 1건 전송

---

## 🧪 수동 테스트 API

```bash
GET /simulate/member
GET /simulate/order
GET /simulate/payment
```

> 시뮬레이터에서 단일 로그 생성 + 스트림에도 전송됨

---

## 🧱 새로운 서비스 추가하기

1. `simulator/{service}.py` 생성

```python
class ReviewSimulator:
    def generate_log(self, now):
        return {"service": "review", "timestamp": now.isoformat(), "log": {...}}

    def render(self, log):
        return json.dumps(log)
```

2. `simulator/__init__.py` 수정

```python
from simulator.review import ReviewSimulator

def get_all_simulators():
    return {
        ...,  # 기존 서비스
        "review": ReviewSimulator()
    }
```

이후 자동으로 `/stream/review`, `/simulate/review` 지원됨.

---

## 🌐 외부 메시지 큐 연동 예시 (Kafka)

```python
# kafka_producer.py
import aiohttp, asyncio, json
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode())

async def consume_stream(service):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://localhost:8000/stream/{service}") as resp:
            async for line in resp.content:
                data = json.loads(line.decode())
                producer.send(f"logs.{service}", data)

asyncio.run(consume_stream("member"))
```

---

## 🐳 Docker 실행 예시

### Dockerfile 예시

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 빌드 및 실행

```bash
docker build -t log-simulator .
docker run -p 8000:8000 log-simulator
```

---

## 🧪 부하 테스트 및 벤치마크

### 5억 건 생성 테스트 기준

- 단일 EC2 인스턴스 (1 vCPU, 2GB RAM 기준)
- `generator.py`에서 TPS 출력 코드 삽입

```python
# generator.py 내부
import time
counter = 0
start = time.time()
...
    counter += 1
    if time.time() - start > 1:
        print(f"Logs/sec: {counter}")
        counter = 0
        start = time.time()
```

### curl 기반 스트림 소비 측정

```bash
curl -N http://localhost:8000/stream > /dev/null
```

> `top`, `htop`, `docker stats` 등으로 CPU/RAM 사용량 측정

---

## 🧭 실행 방법

```bash
uvicorn main:app --reload
```

- `http://localhost:8000/stream` → 전체 로그
- `http://localhost:8000/stream/member` → 특정 서비스 로그
- `http://localhost:8000/docs` → Swagger UI

---

## 📜 라이선스

MIT License

---

## 🙌 작성자

유승주 — 2025

