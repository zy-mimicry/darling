"""
"""

import smtplib
from email.mime.text import MIMEText

from collections import defaultdict
from darling.conf import mail_conf
import re

class MailException(Exception):
    pass

class MailConfTypeErr(MailException):
    pass

class MailTypeErr(MailException):
    pass

class UnvaildEmailErr(MailException):
    pass

class BadEmailFormatErr(MailException):
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

    def load_mail_content(self, cookie_of_mail):
        if isinstance(cookie_of_mail, dict):
            self.subject = cookie_of_mail.get("Subject", "")
            self.message = cookie_of_mail.get("Message", "")
            self.from_addr = cookie_of_mail.get("from_addr", "")
            self.to_addrs = cookie_of_mail.get("to_addrs", [])
            self.headers = cookie_of_mail.get("headers", {})
        else:
            raise MailConfTypeErr("Please input the current type of mail-cookie, that must 'dict'")

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

    def _is_vaild_email(self, email):
        if len(email) > 7:
            if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) == None:
                raise BadEmailFormatErr("Email format is unvaild. please check it.")
        if email not in self.groups_of_email:
            raise UnvaildEmailErr("Your email addr is NOT exists list-of-mails, unvaild.")
        return True

    def _is_vaild_group(self, group):
        if group not in self.emails_of_group:
            raise UnvaildEmailGroupErr("Your group name is NOT exists list-of-groups, unvaild.")
        return True

    def mapping_email_and_group(self, email, group):
        self.emails_of_group[group].add(email)
        self.groups_of_email[email].add(group)

    def unmapping_email_and_group(self, email, group):
        if self._is_vaild_email(email) and self._is_vaild_group(group):
            if self.emails_of_group[group].count == 0:
                del self.emails_of_group[group]
            else:
                self.emails_of_group[group].remove(email)

            if self.groups_of_email[email].count == 0:
                del self.groups_of_email[email]
            else:
                self.groups_of_email[email].remove(group)

    def display_mappings(self):
        print("Mapping emails of group: {}". format(self.emails_of_group))
        print("Mapping groups of email: {}". format(self.groups_of_email))

    def pick_groups_for_email(self, email):
        if self._is_vaild_email(email):
            return self.groups_of_email[email] # the list of groups

    def pick_emails_for_group(self, group):
        if self._is_vaild_group(group):
            return self.emails_of_group[group] # the list of mails

    def emails_in_groups(self, *groups):
        groups = set(groups)
        return (e for (e,g) in self.groups_of_email.items() if g & groups)

import sys

def send_email_to_groups(maillist):
    print("You want to send email from me [{}]: {}".format(sys._getframe().f_code.co_name,maillist))
    pass

def send_email_to_special(maillist):
    print("You want to send email from me [{}]: {}".format(sys._getframe().f_code.co_name,maillist))
    pass

class DarlingMailManager:
    """
    """
    def __init__(self):
        self.registered_mail_lists = defaultdict(set)
        self.marked_mail_lists = defaultdict(set)

    def send(self, send_mail_cb_func = None):
        if send_mail_cb_func != None:
            send_mail_cb_func(self.marked_mail_lists)
        else:
            send_mail_default(self.marked_mail_lists)

    def register_by_name(self, name, maillist):
        self.registered_mail_lists[name].add(maillist)
        print("register")

    def _check_is_registered_by_name(self, name):
        return True if name in self.registered_names else False

    def mark_mail_list_by_name(self, name):
        if self._check_is_registered_by_name(name):
            self.marked_mail_lists[name] = self.registered_mail_lists[name]

    @property
    def registered_names(self):
        return self.registered_mail_lists.keys()
    @property
    def marked_names(self):
        return self.marked_mail_lists.keys()
    pass

    # def send_email(self, dmail, host = "localhost", port = 1025):
    #     if not isinstance(dmail, DarlingMail):
    #         raise MailTypeErr("You must input the instance of DarlingMail.")
    #     headers = {} if dmail.headers is None else dmail.headers

    #     email = MIMEText(dmai.message)
    #     email['Subject'] = dmail.subject
    #     email['From'] = dmail.from_addr
    #     for header,value in dmail.headers.items():
    #         email[header] = value

    #     sender = smtplib.SMTP(host, port)
    #     for addr in set(dmail.to_addrs):
    #         del email['To']
    #         email['To'] = addr
    #         sender.sendmail(from_addr, addr, email.as_string())
    #     sender.quit()

darling_email = None
darling_email_list = None

def configure_email_list(mail_config):
    global darling_email_list, darling_email
    darling_email = DarlingMail()
    darling_email.load_mail_content(mail_config)
    darling_email_list = DarlingMailList()
