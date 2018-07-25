"""
Mail Configuration
"""

default_mail_conf = {
    "subject"      : "Darling Module Init",
    "from_addr"    : "rzheng@sierrawireless.com",
    "to_addrs"     : [
        "1274952282@qq.com",
        "helloworld@sina.com",
        "fuckyou@memeda.com",
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
    """,
}

# You can configure here for sending email.
most_wanted_conf = default_mail_conf

def get_most_wanted():
    return most_wanted_conf
