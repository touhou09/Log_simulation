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

    def render(self, data: dict) -> str:
        return self.template.render(**data)