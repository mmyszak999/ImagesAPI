class IncorrectFileFormat(Exception):
    pass


class UnauthorizedAccountAccess(Exception):
    pass


class ExpiredTokenAccess(Exception):
    pass


class NoExpiringLinkCreatePermission(Exception):
    pass


class IncorrectExpirationTimeEntered(Exception):
    pass