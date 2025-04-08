import asyncio
import random
from datetime import datetime
from simulator import get_all_simulators

TIME_INTERVAL_CONFIG = {
    (0, 7): (2.0, 4.0),
    (8, 11): (1.0, 2.0),
    (12, 13): (0.3, 0.8),
    (14, 18): (1.0, 2.0),
    (19, 23): (1.5, 3.0)
}

def get_interval_by_hour(hour):
    for (start, end), (min_sec, max_sec) in TIME_INTERVAL_CONFIG.items():
        if start <= hour <= end:
            return random.uniform(min_sec, max_sec)
    return 1.0

async def process_service(service, simulator, output_plugin, now):
    log_count = random.randint(100, 250)
    logs = simulator.generate_logs(now, log_count)
    for log in logs:
        rendered = simulator.render(log)
        await output_plugin.write(rendered, topic=f"logs.{service}")
    await asyncio.sleep(random.uniform(0.001, 0.01))

async def start_log_generator(output_plugin):
    simulators = get_all_simulators()
    while True:
        now = datetime.utcnow()
        await asyncio.gather(*[
            process_service(service, simulator, output_plugin, now)
            for service, simulator in simulators.items()
        ])