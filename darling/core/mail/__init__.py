"""
"""

import smtplib
from email.mime.text import MIMEText
from collections import defaultdict
from darling.conf import mail_conf

class MailException(Exception):
    pass

class MailConfTypeErr(MailException):
    pass

class MailTypeErr(MailException):
    pass

class DarlingMail:
    """
    """
    def __init__(self):
        self.subject = ""
        self.message = ""
        self.from_addr = ""
        self.to_addrs = []
        self.headers = {}

    def load_mail_content(self, cooki_of_mail):
        if isinstance(cooki_of_mail, dict):
            self.subject = cooki_of_mail.get("Subject", "")
            self.message = cooki_of_mail.get("Message", "")
            self.from_addr = cooki_of_mail.get("from_addr", "")
            self.to_addrs = cooki_of_mail.get("to_addrs", [])
            self.headers = cooki_of_mail.get("headers", {})
        else:
            raise MailConfTypeErr("Please input the current type of mail-cooki, that must 'dict'")

    def construct_mail(self):
        email = MIMEText(self.message)
        email['Subject'] = self.subject
        email['From'] = self.from_addr
        for header,value in self.headers.items():
            email[header] = value
        email['To'] = self.to_addrs # parse yourself
        return email

class DarlingMailList:
    """\
    \
    """
    def __init__(self):
        self.emails_of_group = defaultdict(set)
        self.groups_of_email = defaultdict(set)

    def map_email_and_group(self, email, group):
        self.emails_of_group[group].append(email)
        self.groups_of_email[email].append(group)

    def emails_in_groups(self, *groups):
        groups = set(groups)
        return (e for (e,g) in self.email_map.items() if g & groups)

    def send_email(self, dmail, host = "localhost", port = 1025):
        if not isinstance(dmail, DarlingMail):
            raise MailTypeErr("You must input the instance of DarlingMail.")
        headers = {} if dmail.headers is None else dmail.headers

        email = MIMEText(dmai.message)
        email['Subject'] = dmail.subject
        email['From'] = dmail.from_addr
        for header,value in dmail.headers.items():
            email[header] = value

        sender = smtplib.SMTP(host, port)
        for addr in set(dmail.to_addrs):
            del email['To']
            email['To'] = addr
            sender.sendmail(from_addr, addr, email.as_string())
        sender.quit()

darling_email = None
darling_email_list = None

def configure_email_list(mail_config):
    global darling_email_list, darling_email
    darling_email = DarlingMail()
    darling_email.load_mail_content(mail_config)
    darling_email_list = DarlingMailList()

