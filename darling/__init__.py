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

    # log(MM.registered_groups)
    # log(MM.registered_servers)

    # log("\n\n\n")

    # mail_01 = Mail(mail_conf.mail_default_conf)
    # mail_02 = Mail(mail_conf.mail_default_conf)

    # group_01 = MailGroup(mail_conf.mail_group_conf)
    # group_02 = MailGroup(mail_conf.mail_group_conf)

    # server_01 = MailServer(mail_conf.mail_server_conf)

    # MM.register_named_mail(mail_01, "rex")
    # MM.register_named_mail(mail_02, "BBB")

    # MM.register_group(group_01)
    # MM.register_group(group_02)

    # MM.register_server(server_01)

    # log(MM.registered_mails)
    # log(MM.registered_groups)
    # log(MM.registered_servers)

    # log(MM.named_mail_lists)

    M1 = Mail(mail_conf.mail_default_conf)
    #G1 = MailGroup(mail_conf.mail_group_conf)
    S1 = MailServer(mail_conf.mail_server_conf_D2)

    MM.register_named_mail(M1, "awesome")
    MM.register_server(S1)

    log("registered server {} ".format(MM.registered_servers))

    MM.mark_mail_by_name("awesome")

    log(MM.to_be_send_ml)

    MM.send()
