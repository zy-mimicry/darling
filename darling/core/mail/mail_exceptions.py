"""
"""

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
