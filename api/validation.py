import imghdr
from typing import Any, OrderedDict

from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile

from api.exceptions import IncorrectFileFormat, UnauthorizedAccountAccess
from api.utils import allowed_formats
from api.models import Account


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