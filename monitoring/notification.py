import datetime

from termcolor import cprint


class Notifier:
    def warning(self, context):
        pass

    def info(self, context):
        pass


class Stdout(Notifier):
    def warning(self, context):
        cprint(f"{datetime.datetime.now()}: "
               f"{context['metric']} = {context['value']}", 'red')

    def info(self, context):
        cprint(f"{datetime.datetime.now()}: "
               f"{context['metric']} = {context['value']}", 'green')

