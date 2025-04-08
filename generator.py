import asyncio
import random
from datetime import datetime, timedelta
from simulator import get_all_simulators
from queue_manager import log_queue

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

async def start_log_generator(output_plugin):
    simulators = get_all_simulators()
    service_times = {
        service: datetime.utcnow().replace(second=0, microsecond=0)
        for service in simulators
    }

    while True:
        for service, simulator in simulators.items():
            now = service_times[service]
            log_count = random.randint(1, 10)
            logs = simulator.generate_logs(now, log_count)

            for log in logs:
                rendered = simulator.render(log)
                await output_plugin.write(rendered, topic=f"logs.{service}")

            # ✅ 여러 로그 생성 후 한 번만 sleep (묶음 단위 지연)
            batch_sleep = get_interval_by_hour(now.hour)
            await asyncio.sleep(batch_sleep)

            service_times[service] += timedelta(seconds=batch_sleep)
