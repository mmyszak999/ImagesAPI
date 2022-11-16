from typing import OrderedDict
from django.contrib.auth.models import User
from rest_framework.fields import CharField

from api.serializers import ImageInputSerializer, ImageMediaSerializer
from api.entities.service_entities import ImageEntity
from api.models import Account, Image, AccountTier


class ImageCreateService:
    """def image_create(self, dto: ImageEntity, account_instance: Account) -> Image:
        return Image.objects.create(
            caption=dto.caption,
            image=dto.image,
            account=account_instance
        )"""

    @classmethod
    def build_dto_from_request_data(cls, request_data: OrderedDict) -> ImageEntity:
        serializer = ImageInputSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        return ImageEntity(
            caption=data["caption"],
            image=data["image"]
        )

    def image_create(self, request_data: OrderedDict, account_instance: Account) -> Image:
        serializer = ImageInputSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        return Image.objects.create(
            caption=data["caption"],
            image_file=data["image_file"],
            account=account_instance
        )


class ImageMediaCreate:

    sizes = []

    def get_account_tier_instance(self, account_pk: int) -> AccountTier:
        instance = Account.objects.get(id=account_pk)
        return instance.account_tier

    def get_thumbnail_sizes_list(self, account_tier: AccountTier) -> list[int]:
        return account_tier.thumbnail_sizes.split(",")

    def check_access_to_original_image(self, account_tier: AccountTier) -> bool:
        return account_tier.original_link

    def create_sizes_schema(self, sizes_list: get_thumbnail_sizes_list, access_to_original: bool, image_instance: Image) -> list:
        if access_to_original:
            self.sizes.append(('full_size', 'url'),)
        for size in sizes_list:
            self.sizes.append((f'{str(size)}px', f'thumbnail__{image_instance.width}x{size}',))
        return self.sizes

