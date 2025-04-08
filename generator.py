
import asyncio
from datetime import datetime, timedelta
from simulator import get_all_simulators
from queue_manager import log_queue

def get_log_count_for_hour(hour):
    if 0 <= hour < 8: return 290
    elif 8 <= hour < 12: return 870
    elif 12 <= hour < 14: return 1160
    elif 14 <= hour < 19: return 1740
    else: return 1740

async def start_log_generator(output_plugin):
    simulators = get_all_simulators()
    now = datetime.utcnow().replace(hour=0, minute=0, second=0)
    while now.hour < 24:
        count = get_log_count_for_hour(now.hour)
        for _ in range(count):
            for service, simulator in simulators.items():
                log = simulator.generate_log(now)
                rendered = simulator.render(log)
                await output_plugin.write(rendered, topic=f"logs.{service}")
        await asyncio.sleep(1)
        now += timedelta(seconds=1)