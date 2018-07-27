# -*- coding: utf-8 -*-

"""
"""

import smtplib, re, sys
from email.mime.text import MIMEText
from darling.conf.mail_conf import get_autoload_conf
from .mail_exceptions import *

def check_mail_format(email_string):
    print(email_string)
    if len(email_string) < 7 and re.match(r"[^@]+@[^@]+\.[^@]+", email_string) == None:
        raise BadEmailFormatErr("Email format is unvaild. please check it.")

class Mail:
    """
    """
    def __init__(self, mail_conf):
        self.name = ""
        self.subject = ""
        self.message = ""
        self.from_addr = ""
        self.to_addrs = []
        self.groups = [] # Just be useful for this class
        self.headers = {}
        self.server_name = ""

        self._load_mail_conf(mail_conf)
        check_mail_format(self.from_addr)
        for addr in self.to_addrs:
            check_mail_format(addr)


    def _load_mail_conf(self,mail_conf):
        if isinstance(mail_conf, dict):
            self.name = mail_conf.get("name", "")
            self.subject = mail_conf.get("subject", "")
            self.message = mail_conf.get("message", "")
            self.from_addr = mail_conf.get("from-addr", "")
            self.to_addrs = mail_conf.get("to-addrs", [])
            self.groups = mail_conf.get("groups", [])
            self.headers = mail_conf.get("headers", {})
            self.server_name = mail_conf.get("server-name","")
        else:
            raise MailConfTypeErr("Please input the current type of mail-cookie, that must 'dict'")

    def _mails_to_strings(self,to_addrs):
        formate_str = ""
        if len(to_addrs) == 0:
            return formate_str
        else:
            for addr in to_addrs:
                if type(addr) == str:
                    formate_str += addr + ","
            return formate_str

    @property
    def construct_mail(self):
        email = MIMEText(self.message)
        email['Subject'] = self.subject
        email['From'] = self.from_addr
        for header,value in self.headers.items():
            email[header] = value
        email['To'] = self._mails_to_strings(self.to_addrs)
        return email

class MailGroup:
    """
    """
    def __init__(self,mail_group_conf):
        self.name = ""
        self.autoload = False
        self.mails = []

        self._load_group_config(mail_group_conf)
        for m in self.mails:
            check_mail_format(m)

    def _load_group_config(self,mail_group_conf):
        if type(mail_group_conf) == dict:
            self.name = mail_group_conf.get('group-name', "")
            self.autoload = mail_group_conf.get('auto-load', False)
            self.mails = mail_group_conf.get('mails', [])
        else:
            raise MailGroupConfTypeErr("The configuration of the mail group should be dict, check it.")

    def is_wanted(self):
        return True if self.autoload == True else False

class MailServer:
    """
    """
    def __init__(self,mail_server_conf):
        self.hostname = "localhost"
        self.ip = "127.0.0.1"
        self.ports = ["8000",]
        self.mark_port = "1025"
        self.password = ""
        self.autoload = False
        self._load_mail_server_config(mail_server_conf)

    def _load_mail_server_config(self,mail_server_conf):
        if type(mail_server_conf) == dict:
            self.hostname = mail_server_conf.get('hostname', "")
            self.ip = mail_server_conf.get('ip', '')
            self.ports = mail_server_conf.get('ports', "")
            self.autoload = mail_server_conf.get('auto-load', False)
            self.mark_port = mail_server_conf.get('mark-port', '')
            self.password = mail_server_conf.get('password', '')
        else:
            raise MailServerConfTypeErr("The configuration of the mail server should be dict, check it.")

    def change_port_in_ports(self, port):
        if str(port) not in self.ports:
            raise UnvaildPortOfMailServer("The port must be configured at init.")
        else:
            self.mark_port = port

    def auto_load(self):
        return True if self.autoload == True else False

class MailManager:
    """
    """
    def __init__(self):
        self.named_mail_lists = {}

        self.registered_mails = {}
        self.registered_groups = []
        self.registered_servers = []

        # Be contained to 'self.named_mail_lists'
        self.to_be_send_ml = {}

        # auto load groups and servers in conf-file.
        self._autoload()

    def _autoload(self):
        (groups_conf, servers_conf) = get_autoload_conf()
        for gc in groups_conf:
            self.register_group(MailGroup(gc))
        for sc in servers_conf:
            self.register_server(MailServer(sc))

    def mark_mail_by_name(self,name):
        if name in self.named_mail_lists.keys():
            self.to_be_send_ml[name] = self.named_mail_lists[name]
        else:
            print("'name' of mail NOT registered before.")

    def register_named_mail(self, mail, name = ""):
        """
        'mail' must be a instance of Mail.
        'name' is the same as the key of self.named_mail_lists.
        """
        if name == "":
            name = mail.name
        else:
            mail.name = name
        self.registered_mails[name] = mail
        self._match(mail, mtype = 'mail')

    def register_group(self, group):
        """
        'group' must be a instance of MailGroup.
        the 'groups' member of Mail should contain the group' name.
        """
        for g in self.registered_groups:
            if g.name == group.name:
                return
        self.registered_groups.append(group)
        self._match(group, mtype = 'group')

    def register_server(self, server):
        """
        'server' must be a instance of MailServer.
        """
        for s in self.registered_servers:
            if server.hostname == s.hostname:
                return
        self.registered_servers.append(server)
        self._match(server, mtype = 'server')
        pass

    def __mail_match(self, mail):
        """
        Finally, must create a MailList instance to map Mail.
        """
        match_group = []
        match_server = None
        for g_name in mail.groups:
            for rg in self.registered_groups:
                if g_name == rg.name:
                    match_group.append(rg)
        for rs in self.registered_servers:
            if mail.server_name == rs.hostname:
                match_server = rs
        self.named_mail_lists[mail.name] = MailList(mail, match_group, match_server)

    def __group_match(self, group):
        """
        match group to mail instance.
        """
        for m in self.registered_mails.values():
            for g_name in m.groups:
                if g_name == group.name:
                    self.named_mail_lists[m.name].registered_groups.append(group)

    def __server_match(self, server):
        """
        match server to mail instance.
        """
        for m in self.registered_mails.values():
            print("mail server name :", m.server_name)
            if m.server_name == server.hostname:
                self.named_mail_lists[m.name].registered_server = server

    def _match(self, item, mtype):
        """
        'mtype' must be one of 'mail', 'group', 'server'.
        """
        if mtype == 'mail':
            self.__mail_match(item)
        elif mtype == 'group':
            self.__group_match(item)
        elif mtype == 'server':
            self.__server_match(item)
        else:
            raise MailMatchTypeErr("The type of match should be {}".format(('mail', 'group','server')))

    def send(self, send_mail_cb_func = None):
        if len(self.to_be_send_ml) == 0:
            print("Marked mail-lists is empty, so can't send.")
            return
        for ml in self.to_be_send_ml.values():
            if send_mail_cb_func != None:
                send_mail_cb_func(ml)
            else:
                send_mail_default(ml)

def send_email_to_groups(maillist):
    print("You want to send email from me [{}]: {}".format(sys._getframe().f_code.co_name,maillist))
    pass

def send_email_to_special(maillist):
    print("You want to send email from me [{}]: {}".format(sys._getframe().f_code.co_name,maillist))
    pass

def send_mail_default(maillist):
    print("You want to send email from me [{}]: {}".format(sys._getframe().f_code.co_name,maillist))
    # sender = smtplib.SMTP("localhost", 1025)
    # sender = smtplib.SMTP(maillist.registered_server.hostname,
    #                       int(maillist.registered_server.mark_port))

    sender = smtplib.SMTP_SSL(maillist.registered_server.hostname,
                          int(maillist.registered_server.mark_port))
    msg   = maillist.registered_mail.construct_mail
    _from = maillist.registered_mail.from_addr
    _to   = msg['To']
    password = maillist.registered_server.password

    sender.login(_from, password)
    sender.sendmail(_from, _to, msg.as_string())
    sender.quit()

class MailList:
    """
    """
    def __init__(self, mail, groups, server):
        if isinstance(mail, Mail) and type(groups) == list:
            self.registered_mail = mail
            self.registered_groups = groups
            self.registered_server = server
        else:
            raise MailListInitErr("Mail-List should be passed\
            [Mail class instance], [list of MailGroup], [MailServer class instance].")

