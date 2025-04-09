from .base import SimulatorBase
from datetime import datetime
from faker import Faker
import random

faker = Faker()

class MemberSimulator(SimulatorBase):
    def __init__(self):
        super().__init__("member_template.json")

    def generate_log(self, now: datetime):
        return {
            "timestamp": now.isoformat(),
            "service": "member",
            "action": random.choice(["register", "login", "logout"]),
            "user_id": faker.uuid4(),
            "ip": faker.ipv4(),
            "latency_ms": random.randint(10, 300),
            "status": 200
        }