
from .base import OutputPluginBase

class FileOutput(OutputPluginBase):
    def __init__(self):
        self.file = open("output.log", "a")

    async def write(self, message: str, topic: str):
        self.file.write(f"[{topic}] {message}\n")
        self.file.flush()