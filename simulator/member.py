from .base import SimulatorBase
from datetime import datetime
import random

class MemberSimulator(SimulatorBase):
    def __init__(self):
        super().__init__("member_template.json")

    def generate_log(self, now: datetime):
        return {
            "timestamp": now.isoformat(),
            "service": "member",
            "action": random.choice(["register", "login", "logout"]),
            "user_id": random.randint(1000, 9999),
            "latency_ms": random.randint(10, 300),
            "ip": f"192.168.0.{random.randint(1, 254)}",
            "status": 200
        }