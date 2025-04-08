from fastapi import FastAPI
from simulator.member import MemberSimulator
from simulator.order import OrderSimulator
from simulator.payment import PaymentSimulator
from datetime import datetime
from queue_manager import log_queue

app = FastAPI()
simulators = {
    "member": MemberSimulator(),
    "order": OrderSimulator(),
    "payment": PaymentSimulator()
}

@app.get("/simulate/{service}")
async def simulate(service: str):
    now = datetime.utcnow()
    simulator = simulators.get(service)
    if not simulator:
        return {"error": "invalid service"}
    log = simulator.generate_log(now)
    await log_queue.put(log)
    return {"queued": log}