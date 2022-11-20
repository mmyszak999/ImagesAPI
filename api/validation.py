import imghdr
from typing import Any, OrderedDict

from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile

from api.exceptions import (
    IncorrectFileFormat, UnauthorizedAccountAccess,
    NoExpiringLinkCreatePermission, IncorrectExpirationTimeEntered
)
from api.utils import allowed_formats
from api.models import Account, AccountTier, Image


class FileValidation:
    def __init__(self, data: OrderedDict, user: User, account_id: int, file: InMemoryUploadedFile) -> None:
        self.data = data
        self.user = user
        self.account_id = account_id
        self.file = file

    def validate_file_format(self):
        file_format = imghdr.what(self.file)
        formats = allowed_formats + [el.upper() for el in allowed_formats]
        if file_format not in formats:
            raise IncorrectFileFormat(f"This type of image format is not allowed!")
        return
    
    def validate_access(self, request_user_id: int, account_id: int):
        account_owner = Account.objects.get(id=account_id).owner
        
        if not (request_user_id == account_owner.id or self.user.is_superuser):
            raise UnauthorizedAccountAccess("You are not the owner of the account!")
        return
    
    def validate_all(self):
        self.validate_file_format()
        self.validate_access(self.user.id, self.account_id)


class ExpiringLinkTokenValidation:
    def __init__(self, request_user: User, account_id: int, seconds: int, image_id: int) -> None:
        self.request_user = request_user
        self.account_id = account_id
        self.seconds = seconds
        self.image_id = image_id
    
    def validate_access_to_create_token(self, account_tier: AccountTier):
        account = Account.objects.get(pk=self.account_id)
        image = Image.objects.get(pk=self.image_id)
        if not (account_tier.expiring_links and self.request_user == account.owner and account == image.account):
            raise NoExpiringLinkCreatePermission(
                "Your account tier does not allow you to create a link or you created a link to the wrong file")
        return
    
    def validate_allowed_time_of_expiration(self, account_tier: AccountTier):

        if not (account_tier.min_expiring_time < int(self.seconds) < account_tier.max_expiring_time):
            raise IncorrectExpirationTimeEntered("Entered expiration time is out of range")
        return
    
    def validate_all(self):
        account_tier = Account.objects.get(id=self.account_id).account_tier
        self.validate_access_to_create_token(account_tier)
        self.validate_allowed_time_of_expiration(account_tier)
