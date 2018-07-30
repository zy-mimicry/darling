"""
Contains all exceptions about mail-core.
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

class MailGroupConfTypeErr(MailException):
    pass

class MailMatchTypeErr(MailException):
    pass

class UnvaildPortOfMailServer:
    pass

class MailServerConfTypeErr:
    pass