from dataclasses import dataclass

from django.core.files.uploadedfile import UploadedFile


@dataclass(frozen=True)
class ImageEntity:
    caption: str
    image_file: UploadedFile


@dataclass(frozen=True)
class ExpiringLinkEntity:
    expires_in: int