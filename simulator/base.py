from abc import ABC, abstractmethod
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from config import TEMPLATE_DIR

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

class SimulatorBase(ABC):
    def __init__(self, template_file):
        self.template = env.get_template(template_file)

    @abstractmethod
    def generate_log(self, now: datetime) -> dict:
        pass

    def generate_logs(self, now: datetime, count: int) -> list:
        return [self.generate_log(now) for _ in range(count)]

    def render(self, data: dict) -> str:
        return self.template.render(**data)