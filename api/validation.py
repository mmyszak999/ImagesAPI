from typing import Any

from django.contrib.auth.models import User

from api.exceptions import IncorrectFileFormat, UnauthorizedAccountAccess
from api.utils import allowed_formats


class FileValidation:
    def __init__(self, data: dict[Any, Any], user: User) -> None:
        self.data = data
        self.user = user

    def validate_file_format(self, file_name: str):
        *rest, format = file_name.split(".")   
        formats = allowed_formats + [el.upper() for el in allowed_formats]
        if format not in formats:
            raise IncorrectFileFormat(f"This type of image format {format} is not allowed!")
        return
    
    def validate_access(self, request_user_id: int, account_owner_id: str):
        if not str(request_user_id) == account_owner_id:
            raise UnauthorizedAccountAccess("You are not the owner of the account!")
        return
    
    def validate_all(self):
        self.validate_file_format(self.data["image_file"].name)
        self.validate_access(self.user.id, self.data["account"])