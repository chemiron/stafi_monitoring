import time

import settings
from monitoring import SystemMonitor
from stafi.monitor import StafiMonitor
from stafi.node import Node as StafiNode


MONITORS = (
    SystemMonitor(settings.CHECK_INTERVAL),
    StafiMonitor(settings.CHECK_INTERVAL,
                 StafiNode(settings.NODE_RPC_URL))
)


if __name__ == '__main__':
    try:
        while True:
            for monitor in MONITORS:
                monitor.process()
            time.sleep(1)
    except KeyboardInterrupt:
        pass
