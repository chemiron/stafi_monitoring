import settings

from monitoring.notification import Stdout
from .node import Node
from .metrics import *

CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 80
DISK_THRESHOLD = 80
NODE_PEERS_THRESHOLD = 20

NOTIFIERS = [
    Stdout(),
]


@cpu_metric.set_alert(*NOTIFIERS)
def cpu_threshold(value):
    return value >= CPU_THRESHOLD


@memory_metric.set_alert(*NOTIFIERS)
def memory_threshold(value):
    return value >= MEMORY_THRESHOLD


@disk_metric.set_alert(*NOTIFIERS)
def disk_threshold(value):
    return value >= DISK_THRESHOLD


@node_peers_metric.set_alert(*NOTIFIERS)
def node_peers_alert(value):
    return value < NODE_PEERS_THRESHOLD


@node_version_metric.set_alert(*NOTIFIERS)
def node_version_alert(value):
    trust_node = Node(settings.TRUST_RPC_URL)
    return value < trust_node.version()


@node_block_height_metric.set_alert(*NOTIFIERS)
def node_block_height_alert(value):
    trust_node = Node(settings.TRUST_RPC_URL)
    return value < trust_node.block_height()
