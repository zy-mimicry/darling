mail_server_conf = {
    "hostname" : "localhost",
    "ip"       : "127.0.0.1",
    "ports"    : [
        1025,
    ]
}

mail_group_conf = {
    "group-name" : "SWI",
    "group-registered" : True,
    "group-emails" : {
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

class Mail:
    pass

class MailGroup:
    pass

class MailManager:
    pass

class MailServer:
    pass
