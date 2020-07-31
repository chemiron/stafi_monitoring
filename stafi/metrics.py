import psutil

from .monitor import StafiMonitor
from monitoring import SystemMonitor


@SystemMonitor.set_metric('cpu')
def cpu_metric(monitor):
    return psutil.cpu_percent(interval=None)


@SystemMonitor.set_metric('memory')
def memory_metric(monitor):
    return psutil.virtual_memory().percent


@SystemMonitor.set_metric('disk')
def disk_metric(monitor):
    return psutil.disk_usage('/').percent


@StafiMonitor.set_metric('node_peers')
def node_peers_metric(monitor):
    return monitor.node.peers()


@StafiMonitor.set_metric('node_version')
def node_version_metric(monitor):
    return monitor.node.version()


@StafiMonitor.set_metric('node_block_height')
def node_block_height_metric(monitor):
    return monitor.node.block_height()
