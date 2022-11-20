from django.urls import reverse
from rest_framework import status

from tests.test_api.test_setup import TestSetUp
from api.exceptions import NoExpiringLinkCreatePermission, ExpiredTokenAccess

class TestExpiringLinkTokenViews(TestSetUp):
    def test_enterprise_user_with_can_create_token(self):
        self.client.force_login(self.enterprise_user)
        self.account = self.accounts[2]
        self.image = self.images[4]
        self.token_data = {
            "image": self.image.id,
            "expires_in": 4321
        }

        response = self.client.post(reverse('api:image-expiring-links', kwargs={
            'pk': self.account.id, 'image_pk': self.image.id
        }), data=self.token_data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_if_user_with_insufficient_tier_cannot_create_a_token(self):
        self.client.force_login(self.basic_user)
        self.account = self.accounts[0]
        self.image = self.images[0]
        self.token_data = {
            "image": self.image.id,
            "expires_in": 1111
        }

        with self.assertRaises(expected_exception=NoExpiringLinkCreatePermission) as exc:
            self.client.post(reverse('api:image-expiring-links', kwargs={
                 'pk': self.account.id, 'image_pk': self.image.id
            }), data=self.token_data)
            

    def test_enterprise_user_with_can_get_tokens(self):
        self.client.force_login(self.enterprise_user)
        self.account = self.accounts[2]

        response = self.client.get(reverse('api:image-expiring-links', kwargs={
            'pk': self.account.id, 'image_pk': self.images[2].id
            }
        ))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

    def test_basic_user_with_can_get_their_tokens(self):
        self.client.force_login(self.basic_user)
        self.account = self.accounts[0]
        self.image = self.images[0]

        response = self.client.get(reverse('api:image-expiring-links', kwargs={
            'pk': self.account.id, 'image_pk': self.images[0].id
            }
        ))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    

    def test_enterprise_user_can_get_image_by_expiring_link(self):
        self.client.force_login(self.enterprise_user)
        self.account = self.accounts[2]
        self.token = self.expiring_link_tokens[0]
        self.image = self.images[2]

        response = self.client.get(reverse('api:image-single-expiring-link', kwargs={
            'pk': self.account.id, 'image_pk': self.image.id, 'token_pk': self.token.id
            }
        ))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

    def test_enterprise_user_cannot_get_image_with_expired_token(self):
        self.client.force_login(self.enterprise_user)
        self.account = self.accounts[2]
        self.token = self.expiring_link_tokens[1]
        self.image = self.images[2]

        with self.assertRaises(expected_exception=ExpiredTokenAccess) as exc:
            self.client.get(reverse('api:image-single-expiring-link', kwargs={
                'pk': self.account.id, 'image_pk': self.image.id, 'token_pk': self.token.id
                }
            ))