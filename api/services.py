from typing import OrderedDict
from django.contrib.auth.models import User

from api.models import Account, Image, AccountTier
from images_api_project.settings import VERSATILEIMAGEFIELD_RENDITION_KEY_SETS
from api.serializers import ImageInputSerializer
from api.validation import FileValidation
from api.entities.api_entities import ImageEntity

class ImageCreateService:
    def __init__(self, request, account_id) -> None:
        self.request = request
        self.account_id = account_id
        
    def validate_file(self):
        file_validation = FileValidation(self.request.data, self.request.user, self.account_id)
        file_validation.validate_all()

    def build_task_dto_from_validated_data(self) -> ImageEntity:
        self.validate_file()
        serializer = ImageInputSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        return ImageEntity(
            caption=data['caption'],
            image_file=data['image_file'],
        )

    def image_create(self) -> Image:
        
        data = self.build_task_dto_from_validated_data()
        return Image.objects.create(
            caption=data.caption,
            image_file=data.image_file,
            account=Account.objects.get(id=self.account_id)
        )


class ImageMediaCreate:
    def __init__(self, sizes: list = []) -> None:
        self.sizes = sizes

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
