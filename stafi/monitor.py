from monitoring import SystemMonitor


class StafiMonitor(SystemMonitor):
    def __init__(self, check_interval, node):
        super(StafiMonitor, self).__init__(check_interval)
        self.node = node

    def get_context(self):
        ctx = super(StafiMonitor, self).get_context()
        ctx['node'] = self.node.name
        return ctx
