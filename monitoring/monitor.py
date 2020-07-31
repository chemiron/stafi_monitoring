import time
import traceback


class Metric:
    def __init__(self, name, method):
        self.name = name
        self.method = method
        self.__alerts = []

    def set_alert(self, *notifiers, delay=0):
        def wrapper(fn):
            alert = Alert(fn, *notifiers, delay=delay)
            self.__alerts.append(alert)
            return alert
        return wrapper

    def __call__(self, monitor):
        value = self.method(monitor)
        context = {
            'monitor': monitor,
            'metric': self.name,
            'value': value,
        }
        for alert in self.__alerts:
            alert(value, context)


class Alert:
    def __init__(self, method, *notifiers, delay=0):
        self.method = method
        self.notifiers = notifiers
        self.delay = delay or 0

        self._last_warning = None

    def __call__(self, value, *, context=None):
        if context is None:
            return

        notify = 'info' if not self.method(value) else 'warning'
        call_ts = time.monotonic()

        if notify == 'info' or call_ts - (self._last_warning or call_ts) > self.delay:
            if notify == 'warning':
                self._last_warning = call_ts
            for notifier in self.notifiers:
                getattr(notifier, notify)(context)


class Monitor:
    __metrics = []

    def __init__(self, check_interval):
        self.check_interval = check_interval
        self._last_processed = time.monotonic()

    def process(self):
        if time.monotonic() - self._last_processed < self.check_interval:
            return

        for metric in self.__metrics:
            try:
                metric(self)
            except Exception:
                traceback.print_exc()

        self._last_processed = time.monotonic()

    @classmethod
    def set_metric(cls, name):
        def wrapper(fn):
            metric = Metric(name, fn)
            cls.__metrics.append(metric)
            return metric
        return wrapper


class SystemMonitor(Monitor):
    pass
