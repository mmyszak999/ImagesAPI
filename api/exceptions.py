class IncorrectFileFormat(Exception):
    pass


class UnauthorizedAccountAccess(Exception):
    pass


class ExpiredAccessToken(Exception):
    pass


class NoExpiringLinkCreatePermission(Exception):
    pass


class IncorrectExpirationTimeEntered(Exception):
    pass