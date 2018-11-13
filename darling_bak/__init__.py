# -*- coding: utf-8 -*-

"""
"""

def setup():
    from darling.utils.log import log, peer
    log("Hello, Logging module.")
    peer("I am super man.")

    from darling.conf import mail_conf
    from darling.core.mail.mail import (
        Mail,
        MailList,
        MailServer,
        MailGroup,
        MailManager,

        send_mail_default,
        send_email_to_special,
        send_email_to_groups,
    )

    MM = MailManager()

    M1 = Mail(mail_conf.mail_default_conf)
    #G1 = MailGroup(mail_conf.mail_group_conf)
    S1 = MailServer(mail_conf.mail_server_conf_D2)

    MM.register_named_mail(M1, "awesome")
    MM.register_server(S1)

    log("registered server {} ".format(MM.registered_servers))

    MM.mark_mail_by_name("awesome")

    log(MM.to_be_send_ml)

    MM.send()
