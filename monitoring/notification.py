import datetime
import smtplib

from email.message import EmailMessage
from termcolor import cprint

import settings


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


class Email(Notifier):
    sender = None
    recipients = None
    email_template = None
    title_template = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @property
    def smtp_server(self):
        server = getattr(self, '_smtp_server', None)
        if server is None:
            smtp_settings = settings.SMTP_SERVER.copy()
            is_ssl = smtp_settings.pop('ssl', False)
            username = smtp_settings.pop('login', None)
            password = smtp_settings.pop('password', None)

            smtp_cls = smtplib.SMTP if not is_ssl else smtplib.SMTP_SSL
            server = smtp_cls(**settings.SMTP_SERVER)
            if username is not None:
                server.login(username, password)
            setattr(self, '_smtp_server', server)

        return server

    def warning(self, context):
        assert self.email_template is not None, "Email has empty template"

        title = "Warning"
        if self.title_template is not None:
            with open(self.title_template) as fp:
                title = fp.read().format(**context)

        with open(self.email_template) as fp:
            body = fp.read().format(**context)

        self._send_emails(title, body)

    def _send_emails(self, title, body):
        for recipient in self.recipients or []:
            msg = EmailMessage()
            msg.set_content(body)
            msg['Subject'] = title
            msg['From'] = self.sender
            msg['To'] = recipient

            s = self.smtp_server
            s.send_message(msg)
