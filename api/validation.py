from django.contrib.auth.models import User
from rest_framework.request import Request

from api.exceptions import IncorrectFileFormat, UnauthorizedAccountAccess


class FileValidation:
    def __init__(self, data: dict, request: Request) -> None:
        self.data = data
        self.request = request

    def validate_file_format(self, file_name: str):
        _, format = file_name.split(".")    
        if format not in ["JPG", "JPEG", "PNG"]:
            raise IncorrectFileFormat
    
    def validate_access(self, request_user_id: int, account_owner: User):
        if not request_user_id == account_owner:
            raise UnauthorizedAccountAccess
    
    def validate_all(self):
        self.validate_file_format(self.data["image_file"])
        self.validate_access(self.request.user.id, self.data["account"])