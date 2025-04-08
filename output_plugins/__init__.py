
from config import OUTPUT_METHOD
from .stdout_output import StdoutOutput
from .file_output import FileOutput
from .kafka_output import KafkaOutput

def get_output_plugin():
    if OUTPUT_METHOD == "kafka":
        return KafkaOutput()
    elif OUTPUT_METHOD == "file":
        return FileOutput()
    else:
        return StdoutOutput()
