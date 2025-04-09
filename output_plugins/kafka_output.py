from .base import OutputPluginBase
from kafka import KafkaProducer
import json
from config import KAFKA_BOOTSTRAP_SERVERS

class KafkaOutput(OutputPluginBase):
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )

    async def write(self, message: str, topic: str):
        self.producer.send(topic, json.loads(message))