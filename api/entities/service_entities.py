from dataclasses import dataclass

from api.models import Image


@dataclass(frozen=True)
class ImageEntity:
    caption: str
    image: Image.image_file


