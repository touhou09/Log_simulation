from .base import SimulatorBase
from datetime import datetime
from faker import Faker
import random

faker = Faker()

class PaymentSimulator(SimulatorBase):
    def __init__(self):
        super().__init__("payment_template.json")

    def generate_log(self, now: datetime):
        return {
            "timestamp": now.isoformat(),
            "service": "payment",
            "action": random.choice(["pay", "refund", "status"]),
            "payment_id": faker.uuid4(),
            "ip": faker.ipv4(),
            "latency_ms": random.randint(15, 400),
            "status": 200
        }