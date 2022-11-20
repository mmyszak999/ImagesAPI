from tests.test_api.test_setup import TestSetUp
from api.services import GetTokenImageService
from api.models import ExpiringLinkToken
from api.exceptions import ExpiredTokenAccess


class TestGetTokenImageService(TestSetUp):
    def test_service_correctly_get_image_by_token_for_enterprise_user(self):
        self.client.force_login(self.enterprise_user)
        self.account = self.accounts[2]
        self.image = self.images[2]
        self.token = self.expiring_link_tokens[0]
        
        service = GetTokenImageService(self.token.id)
        token_image = service.get_token_image()

        self.assertEqual(token_image, self.image)
        self.assertEqual(token_image.account, self.account)
    

    def test_service_correctly_raises_exception_for_expired_token_for_enterprise_user(self):
        self.client.force_login(self.enterprise_user)
        self.account = self.accounts[0]
        self.image = self.images[2]
        self.token = self.expiring_link_tokens[1]
        
        service = GetTokenImageService(self.token.id)

        with self.assertRaises(expected_exception=ExpiredTokenAccess):
            service.get_token_image()


