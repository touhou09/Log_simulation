from .base import SimulatorBase
from datetime import datetime
import random

class PaymentSimulator(SimulatorBase):
    def __init__(self):
        super().__init__("payment_template.json")

    def generate_log(self, now: datetime):
        return {
            "timestamp": now.isoformat(),
            "service": "payment",
            "action": random.choice(["pay", "refund", "status"]),
            "payment_id": random.randint(100000, 999999),
            "latency_ms": random.randint(15, 400),
            "ip": f"172.16.0.{random.randint(1, 254)}",
            "status": 200
        }
