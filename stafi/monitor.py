from monitoring import Monitor


class StafiMonitor(Monitor):
    def __init__(self, check_interval, node):
        super(StafiMonitor, self).__init__(check_interval)
        self.node = node
