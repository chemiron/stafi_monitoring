import socket
import time
import traceback

import settings


class Metric:
    def __init__(self, name, method):
        self.name = name
        self.method = method
        self.__alerts = []

    def set_alert(self, notifier, **kwargs):
        def wrapper(fn):
            alert = Alert(fn, notifier, **kwargs)
            self.__alerts.append(alert)
            return fn
        return wrapper

    def __call__(self, monitor, context):
        context.update({
            'monitor': monitor,
            'metric': self.name,
        })
        value = self.method(monitor, context)
        context['value'] = value
        for alert in self.__alerts:
            alert(value, context=context.copy())


class Alert:
    def __init__(self, method, *notifiers, delay=0,
                 sleep=settings.WARNING_REPEAT):
        self.method = method
        self.notifiers = notifiers
        self.delay = delay or 0
        self.sleep = sleep

        self._last_warning = None
        self._next_warning = None

    def __call__(self, value, context=None):
        if context is None:
            return

        notify = 'info' if not self.method(value, context) else 'warning'
        call_ts = time.monotonic()

        sent = False
        if (notify == 'info' or
                (call_ts - (self._last_warning or call_ts) >= self.delay
                 and call_ts - (self._next_warning or call_ts) >= 0)):
            for notifier in self.notifiers:
                getattr(notifier, notify)(context)
            sent = True

        if notify == 'warning':
            self._last_warning = call_ts if sent else self._last_warning
            if sent:
                self._next_warning = call_ts + self.sleep
        else:
            self._last_warning = None


class MonitorType(type):
    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls._metrics = []


class Monitor(metaclass=MonitorType):
    def __init__(self, check_interval):
        self.check_interval = check_interval
        self._last_processed = time.monotonic()

    def process(self):
        if time.monotonic() - self._last_processed < self.check_interval:
            return

        for metric in self._metrics:
            try:
                metric(self, self.get_context())
            except Exception:
                traceback.print_exc()

        self._last_processed = time.monotonic()

    @classmethod
    def set_metric(cls, name):
        def wrapper(fn):
            metric = Metric(name, fn)
            cls._metrics.append(metric)
            return metric
        return wrapper

    def get_context(self):
        return {
            "host": socket.gethostname(),
        }


class SystemMonitor(Monitor):
    pass
