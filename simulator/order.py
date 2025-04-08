from .base import SimulatorBase
from datetime import datetime
import random

class OrderSimulator(SimulatorBase):
    def __init__(self):
        super().__init__("order_template.json")

    def generate_log(self, now: datetime):
        return {
            "timestamp": now.isoformat(),
            "service": "order",
            "action": random.choice(["create", "cancel", "status"]),
            "order_id": random.randint(10000, 99999),
            "latency_ms": random.randint(20, 500),
            "ip": f"10.0.0.{random.randint(1, 254)}",
            "status": 200
        }