import os

import settings

from monitoring.notification import Stdout, Email
from .node import Node
from .metrics import *

CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 80
DISK_THRESHOLD = 80
NODE_PEERS_THRESHOLD = 20

PATH = os.path.dirname(os.path.abspath(__file__))


class EmailAlert(Email):
    sender = settings.EMAIL_SENDER
    recipients = settings.EMAIL_RECIPIENTS


class ThresholdEmail(EmailAlert):
    email_template = os.path.join(PATH, 'emails/threshold.tmpl')
    title_template = os.path.join(PATH, 'emails/threshold_title.tmpl')


class PeersEmail(EmailAlert):
    email_template = os.path.join(PATH, 'emails/peers.tmpl')
    title_template = os.path.join(PATH, 'emails/peers_title.tmpl')


class BestNodeEmail(EmailAlert):
    email_template = os.path.join(PATH, 'emails/best_node.tmpl')
    title_template = os.path.join(PATH, 'emails/best_node_title.tmpl')


#######################################
# ALERTS
@cpu_metric.set_alert(Stdout(), ThresholdEmail())
def cpu_threshold(value, context):
    context['threshold'] = CPU_THRESHOLD
    return value >= CPU_THRESHOLD


@memory_metric.set_alert(Stdout(), ThresholdEmail())
def memory_threshold(value, context):
    context['threshold'] = MEMORY_THRESHOLD
    return value >= MEMORY_THRESHOLD


@disk_metric.set_alert(Stdout(), ThresholdEmail())
def disk_threshold(value, context):
    context['threshold'] = DISK_THRESHOLD
    return value >= DISK_THRESHOLD


@node_peers_metric.set_alert(Stdout(), PeersEmail())
def node_peers_alert(value, context):
    context['threshold'] = NODE_PEERS_THRESHOLD
    return value < NODE_PEERS_THRESHOLD


@node_version_metric.set_alert(Stdout(), BestNodeEmail())
def node_version_alert(value, context):
    trust_node = Node(settings.TRUST_RPC_URL)
    context[f'best_value'] = trust_node.version()
    return value < context['best_value']


@node_block_height_metric.set_alert(Stdout(), BestNodeEmail())
def node_block_height_alert(value, context):
    trust_node = Node(settings.TRUST_RPC_URL)
    context[f'best_value'] = trust_node.block_height()
    return value < context['best_value']


@node_online_metric.set_alert(BestNodeEmail())
def node_offline_alert(value, context):
    return not value
