from random import randint
import os

from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from api.models import AccountTier, Account, Image
from ImagesAPIproject.settings import BASE_DIR


class TestSetUp(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # create test users
        cls.basic_user = User.objects.create(username='basic_user')
        cls.premium_user = User.objects.create(username='premium_user')
        cls.enterprise_user = User.objects.create(username='enterprise_user')
        cls.custom_user = User.objects.create(username='custom_user')
        cls.super_user = User.objects.create_superuser(username="superuser")

        cls.account_tiers = AccountTier.objects.bulk_create([
            AccountTier(
                tier_name="basic", thumbnail_sizes="200",
                original_link=False, expiring_links=False,
                min_expiring_time=0, max_expiring_time=0
            ),
            AccountTier(
                tier_name="premium", thumbnail_sizes="200,400",
                original_link=True, expiring_links=False,
                min_expiring_time=0, max_expiring_time=0
            ),
            AccountTier(
                tier_name="enterprise", thumbnail_sizes="200,400",
                original_link=True, expiring_links=True,
                min_expiring_time=300, max_expiring_time=30000
            ),
            AccountTier(
                tier_name="custom", thumbnail_sizes="100,300",
                original_link=True, expiring_links=False,
                min_expiring_time=0, max_expiring_time=0
            )
        ])

        cls.accounts = Account.objects.bulk_create([
            Account(owner=cls.basic_user,
                    account_tier=cls.account_tiers[0]),
            Account(owner=cls.premium_user,
                    account_tier=cls.account_tiers[1]),
            Account(owner=cls.enterprise_user,
                    account_tier=cls.account_tiers[2]),
            Account(owner=cls.custom_user,
                    account_tier=cls.account_tiers[3]),
        ])

        cls.prepare_images = {
            'basic':(open(os.path.join(BASE_DIR, 'tests/test_images/basicuser.PNG'), "rb")),
            "premium": (open(os.path.join(BASE_DIR, 'tests/test_images/premiumuser.JPG'), "rb")),
            "enterprise": (open(os.path.join(BASE_DIR, 'tests/test_images/enterpriseuser.JPG'), "rb")),
            "custom": (open(os.path.join(BASE_DIR, 'tests/test_images/customuser.PNG'), "rb")),
            "to_upload": os.path.join(BASE_DIR, 'tests/test_images/imagetoupload.JPG'),
            "wrong_format": (open(os.path.join(BASE_DIR, 'tests/test_images/wrongimageformat.GIF'), "rb")),
        }

        cls.images = Image.objects.bulk_create([
            Image(
                image_file=SimpleUploadedFile(
                name=cls.prepare_images["basic"].name,
                content=cls.prepare_images["basic"].read(),
                content_type='image/png'
            ),
                caption="basicuser_image",
                account=cls.accounts[0]
            ),
            Image(image_file=SimpleUploadedFile(
                name=cls.prepare_images["premium"].name,
                content=cls.prepare_images["premium"].read(),
                content_type='image/jpg'
            ),
                caption="premiumuser_image",
                account=cls.accounts[1]
                ),
            Image(image_file=SimpleUploadedFile(
                name=cls.prepare_images["enterprise"].name,
                content=cls.prepare_images["enterprise"].read(),
                content_type='image/jpg'
            ),
                caption="enterpriseuser_image",
                account=cls.accounts[2]
                ),
            Image(image_file=SimpleUploadedFile(
                name=cls.prepare_images["custom"].name,
                content=cls.prepare_images["custom"].read(),
                content_type='image/png'
            ),
                caption="customuser_image",
                account=cls.accounts[3]
            ),  
        ])

    def setUp(self) -> None:
        self.client.force_login(self.super_user)

