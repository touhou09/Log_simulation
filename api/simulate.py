from fastapi import APIRouter
from simulator.member import MemberSimulator
from simulator.order import OrderSimulator
from simulator.payment import PaymentSimulator
from datetime import datetime
from stream_queue import publish_to_streams

router = APIRouter()

simulators = {
    "member": MemberSimulator(),
    "order": OrderSimulator(),
    "payment": PaymentSimulator()
}

@router.get("/simulate/{service}")
async def simulate(service: str):
    now = datetime.utcnow()
    simulator = simulators.get(service)
    if not simulator:
        return {"error": "invalid service"}
    log = simulator.generate_log(now)
    await publish_to_streams(service, simulator.render(log))
    return {"queued": log}