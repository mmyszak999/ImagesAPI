from typing import OrderedDict
from django.db import transaction

from api.models import Account, Image, AccountTier
from ImagesAPIproject.settings import VERSATILEIMAGEFIELD_RENDITION_KEY_SETS
from api.serializers import ImageInputSerializer

"""class ImageCreateService:

    @transaction.atomic()
    def image_create(self, account_instance: Account, request_data) -> Image:
        serializer = ImageInputSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        print(data['caption'])

        return Image.objects.create(
            caption=data['caption'],
            image_file=data['image_file'],
            account=account_instance
        )

        serializer = ImageInputSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
"""


class ImageMediaCreate:
    sizes = []

    def get_account_tier_instance(self, account_pk: int) -> AccountTier:
        instance = Account.objects.get(id=account_pk)
        return instance.account_tier

    def get_thumbnail_sizes_list(self, account_tier: AccountTier) -> list:
        return account_tier.thumbnail_sizes.split(",")

    def check_access_to_original_image(self, account_tier: AccountTier) -> bool:
        return account_tier.original_link

    def create_sizes_schema(self, account_id: int, image_instance: Image) -> list:
                
        account_tier = self.get_account_tier_instance(account_id)
        sizes_list = self.get_thumbnail_sizes_list(account_tier)
        access_to_original = self.check_access_to_original_image(account_tier)

        actual_sizes = VERSATILEIMAGEFIELD_RENDITION_KEY_SETS['media_sizes']

        if not actual_sizes:
            if AccountTier.original_link and access_to_original:
                self.sizes.append(('full_size', 'url'), )
            for size in sizes_list:
                self.sizes.append((f'{str(size)}', f'thumbnail__{image_instance.width}x{size}',))
            return self.sizes

        else:
            if access_to_original:
                if ('full_size', 'url') not in actual_sizes:
                    actual_sizes.append(('full_size', 'url'))
            else:
                if ('full_size', 'url') in actual_sizes:
                    actual_sizes.remove(('full_size', 'url'))

            wrongs = []
            for _, element in enumerate(actual_sizes):
                if element == ('full_size', 'url'):
                    continue
                if str(element[0]) not in sizes_list:
                    wrongs.append(tuple(element))
            for element in wrongs:
                actual_sizes.remove(element)
            for size in sizes_list:
                actual_sizes.append((f'{str(size)}', f'thumbnail__{image_instance.width}x{size}',))

            return actual_sizes
