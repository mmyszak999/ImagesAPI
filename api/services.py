from datetime import timedelta

from rest_framework.request import Request
from django.utils import timezone

from images_api_project.settings import VERSATILEIMAGEFIELD_RENDITION_KEY_SETS
from api.models import Account, Image, AccountTier, ExpiringLinkToken
from api.serializers import ImageInputSerializer, ExpringLinkTokenInputSerializer
from api.validation import FileValidation, ExpiringLinkTokenValidation
from api.entities.api_entities import ImageEntity, ExpiringLinkEntity
from api.exceptions import ExpiredTokenAccess


class ImageCreateService:
    def __init__(self, request: Request, account_id: int) -> None:
        self.request = request
        self.account_id = account_id
        
    def validate_file(self):
        file_validation = FileValidation(self.request.data,
        self.request.user, self.account_id, self.request.FILES['image_file']
        )
        file_validation.validate_all()

    def build_image_dto_from_validated_data(self) -> ImageEntity:
        self.validate_file()
        serializer = ImageInputSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        return ImageEntity(
            caption=data['caption'],
            image_file=data['image_file'],
        )

    def image_create(self) -> Image:
        data = self.build_image_dto_from_validated_data()
        return Image.objects.create(
            caption=data.caption,
            image_file=data.image_file,
            account=Account.objects.get(id=self.account_id)
        )


class ImageMediaCreateService:
    def __init__(self, sizes=None) -> None:
        if sizes is None:
            sizes = []
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
            self.sizes = actual_sizes

            return self.sizes


class ExpringLinkCreateService:
    def __init__(self, request: Request, image_id: int, account_id: int) -> None:
        self.request = request
        self.image_id = image_id
        self.account_id = account_id

    def validate_access_to_create_token(self):
        expiring_link_token_validation = ExpiringLinkTokenValidation(
            self.request.user, self.account_id, self.request.data["expires_in"], self.image_id
            )
        expiring_link_token_validation.validate_all()

    def build_task_dto_from_validated_data(self) -> ExpiringLinkEntity:
        self.validate_access_to_create_token()
        serializer = ExpringLinkTokenInputSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        return ExpiringLinkEntity(
            expires_in=data["expires_in"],
        )

    def expiring_link_create(self) -> ExpiringLinkToken:
        link_entity = self.build_task_dto_from_validated_data()
        expiration_date = timezone.now() + timedelta(seconds=link_entity.expires_in)
        image = Image.objects.get(id=self.image_id)

        return ExpiringLinkToken.objects.create(
            expiration_date=expiration_date,
            image=image,
            expires_in=link_entity.expires_in
        )


class GetTokenImageService:
    def __init__(self, token_id: int) -> None:
        self.token_id = token_id

    def validate_token(self, access_token: ExpiringLinkToken):
        if access_token.expiration_date < timezone.now():
            access_token.delete()
            raise ExpiredTokenAccess("Token has expired")
        return
    
    def get_token_image(self) -> Image:
        access_token = ExpiringLinkToken.objects.get(id=self.token_id)
        self.validate_token(access_token)
        return access_token.image