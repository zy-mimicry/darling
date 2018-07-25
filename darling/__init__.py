# -*- coding: utf-8 -*-

"""
"""

def setup():
    from darling.utils.log import log, peer
    log("Hello, Logging module.")
    peer("I am super man.")

    from darling.core import mail
    from darling.conf import get_most_wanted
    m1 = mail.Mail()
    m2 = mail.Mail()

    ml1 = mail.MailingList()
    ml2 = mail.MailingList()

    ml1.mapping_email_and_group(m1, "rex")
    ml1.mapping_email_and_group(m2, "mm")
    ml1.mapping_email_and_group(m2, "rex")

    ml2.mapping_email_and_group(m1, "fuck")
    ml2.mapping_email_and_group(m1, "tty")
    ml2.mapping_email_and_group(m2, "mm")

    ml1.display_mappings()
    ml2.display_mappings()

    mm = mail.MailManager()
    mm.register_by_name("memeda", ml1)
    mm.register_by_name("hahaha", ml2)

    log(mm.registered_names)
    log(mm.marked_names)

    mm.mark_mail_list_by_name("memeda")

    mm.send(get_most_wanted())


