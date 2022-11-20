from tests.test_api.test_setup import TestSetUp
from api.services import ImageMediaCreateService
from api.models import Image


class TestImageMediaCreateService(TestSetUp):
    def test_service_correctly_creates_thumbnail_schema_for_basic_user(self):
        self.client.force_login(self.basic_user)
        self.account = self.accounts[0]
        self.image = self.images[0]
        service = ImageMediaCreateService()
        sizes_schema = service.create_sizes_schema(self.account.id, self.image)

        self.assertEqual(len(sizes_schema), 1)
        self.assertEqual(type(sizes_schema), list)
    

    def test_service_correctly_creates_thumbnail_schema_for_premium_user(self):
        self.client.force_login(self.premium_user)
        self.account = self.accounts[1]
        self.image = self.images[1]
        service = ImageMediaCreateService()
        sizes_schema = service.create_sizes_schema(self.account.id, self.image)

        self.assertEqual(len(sizes_schema), 3)
        self.assertEqual(type(sizes_schema), list)
    

    def test_service_correctly_creates_thumbnail_schema_for_enterprise_user(self):
        self.client.force_login(self.enterprise_user)
        self.account = self.accounts[2]
        self.image = self.images[2]
        service = ImageMediaCreateService()
        sizes_schema = service.create_sizes_schema(self.account.id, self.image)

        self.assertEqual(len(sizes_schema), 3)
        self.assertEqual(type(sizes_schema), list)