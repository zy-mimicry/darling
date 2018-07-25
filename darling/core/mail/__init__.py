"""
"""

import smtplib, re, sys
from email.mime.text import MIMEText

from collections import defaultdict
from darling.conf import mail_conf

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



class Mail:
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
            self.subject = cookie_of_mail.get("subject", "")
            self.message = cookie_of_mail.get("message", "")
            self.from_addr = cookie_of_mail.get("from_addr", "")
            self.to_addrs = cookie_of_mail.get("to_addrs", [])
            self.headers = cookie_of_mail.get("headers", {})
        else:
            raise MailConfTypeErr("Please input the current type of mail-cookie, that must 'dict'")

    def _check_email_format(self, email_string):
        if len(email_string) < 7 and re.match(r"[^@]+@[^@]+\.[^@]+", email_string) == None:
            raise BadEmailFormatErr("Email format is unvaild. please check it.")
        return True

    def check_email_format(self):
        """ Check the 'from_addr' and 'to_addrs' format. """
        self._check_email_format(self.from_addr)
        for e in self.to_addrs:
            self._check_email_format(e)
        return True

    @property
    def construct_mail(self):
        email = MIMEText(self.message)
        email['Subject'] = self.subject
        email['From'] = self.from_addr
        for header,value in self.headers.items():
            email[header] = value
        email['To'] = self.to_addrs # parse yourself
        return email

class MailingList:
    """
    """
    def __init__(self):
        self.emails_of_group = defaultdict(set)
        self.groups_of_email = defaultdict(set)

    def _is_vaild_email(self, email):
        if email.check_email_format():
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
            self.emails_of_group[group].remove(email)
            if len(self.emails_of_group[group]) == 0:
                del self.emails_of_group[group]
            self.groups_of_email[email].remove(group)
            if len(self.groups_of_email[email]) == 0:
                del self.groups_of_email[email]

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
        return [e for (e,g) in self.groups_of_email.items() if g & groups]

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

def send_email_to_groups(maillist):
    print("You want to send email from me [{}]: {}".format(sys._getframe().f_code.co_name,maillist))
    pass

def send_email_to_special(maillist):
    print("You want to send email from me [{}]: {}".format(sys._getframe().f_code.co_name,maillist))
    pass

def send_mail_default(maillist, cookie):
    print("You want to send email from me [{}]: {}".format(sys._getframe().f_code.co_name,maillist))
    to_be_send_mails = maillist.groups_of_email.keys()
    sender = smtplib.SMTP("localhost", 1025)
    for e in to_be_send_mails:
        e.load_mail_content(cookie)
        m = e.construct_mail
        for addr in set(e.to_addrs):
            del m['To']
            m['To'] = addr
            sender.sendmail(e.from_addr, addr, m.as_string())
    sender.quit()

class MailManager:
    """
    """
    def __init__(self):
        self.registered_mail_lists = defaultdict(set)
        self.marked_mail_lists = defaultdict(set)

    def send(self, email_cookie, send_mail_cb_func = None):
        if len(self.marked_mail_lists) == 0:
            print("Marked mail lists is empty, so can't send.")
            return
        for list_of_maillist in self.marked_mail_lists.values():
            for maillist in list_of_maillist:
                if send_mail_cb_func != None:
                    send_mail_cb_func(maillist, email_cookie)
                else:
                    send_mail_default(maillist, email_cookie)

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

