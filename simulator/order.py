from .base import SimulatorBase
from datetime import datetime
from faker import Faker
import random

faker = Faker()

class OrderSimulator(SimulatorBase):
    def __init__(self):
        super().__init__("order_template.json")

    def generate_log(self, now: datetime):
        return {
            "timestamp": now.isoformat(),
            "service": "order",
            "action": random.choice(["create", "cancel", "status"]),
            "order_id": faker.uuid4(),
            "ip": faker.ipv4(),
            "latency_ms": random.randint(20, 500),
            "status": 200
        }