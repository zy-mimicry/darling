# -*- coding: utf-8 -*-

"""
"""

mail_server_conf = {
    "hostname" : "localhost",
    "ip"       : "127.0.0.1",
    "server-registered" : True,
    "mark-port": "1025"
    "ports"    : [
        "8000",
        "1025",
    ]
}

mail_group_conf = {
    "group-name" : "SWI",
    "group-registered" : True,
    "mails" : {
        "1274928808@qq.com",
        "helloworld@sina.com",
    }
}

mail_conf = {
    "subject"      : "Darling Module Init",
    "from_addr"    : "rzheng@sierrawireless.com",
    "to_addrs"     : [
        "1274952282@qq.com",
        "helloworld@sina.com",
        "fuckyou@memeda.com",
    ],
    "groups" : [
        "SWI",
        "baidu-group"
    ],
    "headers"      : {
        "first_stage" : "first stage",
        "second_stage" : "second stage",
    },
    "message"      :\
    """
    Dear everyone,

    The Darling Module Test package is very useful.

    If you want to test some case for yourself,
    you can try it.

    You will enjoy it I think.

    Thx.
    Rex Z
    """
}

from .mail_exceptions import *

def check_mail_format(email_string):
    if len(email_string) < 7 and re.match(r"[^@]+@[^@]+\.[^@]+", email_string) == None:
        raise BadEmailFormatErr("Email format is unvaild. please check it.")

class Mail:
    """
    """
    def __init__(self, mail_conf):
        self.subject = ""
        self.message = ""
        self.from_addr = ""
        self.to_addrs = []
        self.groups = [] # Just be useful for this class
        self.headers = {}

        self._load_mail_conf(mail_conf)
        check_mail_format(self.from_addr)
        for addr in self.to_addrs:
            check_mail_format(addr)


    def _load_mail_conf(self,mail_conf):
        if isinstance(mail_conf, dict):
            self.subject = mail_conf.get("subject", "")
            self.message = mail_conf.get("message", "")
            self.from_addr = mail_conf.get("from_addr", "")
            self.to_addrs = mail_conf.get("to_addrs", [])
            self.groups = mail_conf.get("groups", [])
            self.headers = mail_conf.get("headers", {})
        else:
            raise MailConfTypeErr("Please input the current type of mail-cookie, that must 'dict'")

    def _Toaddrs_to_str(self,to_addrs):
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
        email['To'] = self._Toaddrs_to_str(self.to_addrs)
        return email


class MailGroup:
    def __init__(self,mail_group_conf):
        self.name = ""
        self.registered = False
        self.mails = []
        self._load_group_config(mail_group_conf)
        for m in self.mail_group['mails']:
            check_mail_format(m)

    def _load_group_config(self,mail_group_conf):
        if type(mail_group_conf) == dict:
            self.name = mail_group_conf['group-name']
            self.registered = mail_group_conf['group-registered']
            self.mails = mail_group_conf['mails']
        else:
            raise MailGroupConfTypeErr("The configuration of the mail group should be dict, check it.")

    def is_wanted(self):
        return True if self.registered == True else False

class MailManager:
    """
    """
    def __init__(self):
        self.named_mail_lists = {}
        self.registered_mails = {}
        self.registered_groups = []

        self.to_be_send_ml = {}

    def register_named_mail(self, name, mail):
        self.registered_mails[name] = mail
        self._match(mail, mtype = 'mail')

    def register_group(self, group):
        self.registered_groups.append(group)
        self._match(group, mtype = 'group')

    def __mail_match(self, mail):
        match_group = []
        for g_name in mail.groups:
            for rg in self.registered_groups:
                if g_name == rg.name:
                    match_group.append(rg)
        self.named_mail_lists[mail.name] = MailList(mail, match_group)

    def __match_group(self, group):
        for m in self.registered_mails.values():
            for g_name in m.groups:
                if g_name == group.name:
                    self.named_mail_lists[m.name].registered_mail_group.append(group)

    def _match(self, item, mtype = 'mail'):
        if mtype == 'mail':
            self.__mail_match(item)
        elif mtype == 'group':
            self.__group_match(item)
        else:
            raise MailMatchTypeErr("The type of match should be {}".format(('mail', 'group')))

    def send():
        if len(self.named_mail_lists) == 0:
            print("Registered mail-lists is empty, so can't send.")
            return
        for ml in self.named_mail_lists.values():
            if send_mail_cb_func != None:
                send_mail_cb_func(ml)
            else:
                send_mail_default(ml)

class MailList:
    """
    """
    def __init__(self, mail, groups):
        if isinstance(mail, Mail) and type(groups) == list:
            self.registered_mail = mail
            self.registered_groups = groups
        else:
            raise MailListInitErr("Mail-List should be passed [Mail class isinstance] and [list of MailGroup].")

class MailServer:
    """
    """
    def __init__(self,mail_server_conf):
        self.hostname = "localhost"
        self.ip = "127.0.0.1"
        self.ports = ["8000",]
        self.mark_port = "1025"
        self._load_mail_server_config(mail_server_conf)

    def _load_mail_server_config(self,mail_server_conf):
        if type(mail_server_conf) == dict:
            self.hostname = mail_server_conf['hostname']
            self.ip = mail_server_conf['ip']
            self.ports = mail_server_conf['ports']
            self.registered = mail_server_conf['server-registered']
            self.mark_port = mail_server_sonc['mark-port']
        else:
            raise MailServerConfTypeErr("The configuration of the mail server should be dict, check it.")

    def change_port_in_ports(self, port):
        if str(port) not in self.ports:
            raise UnvaildPortOfMailServer("The port must be configured at init.")
        else:
            self.mark_port = port

    def is_wanted(self):
        return True if self.registered == True else False
