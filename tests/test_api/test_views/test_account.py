from django.urls import reverse
from rest_framework import status

from tests.test_api.test_setup import TestSetUp


class TestAccountViews(TestSetUp):
    def test_if_admin_can_get_all_accounts(self):
            
        response = self.client.get(reverse('api:account-accounts'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
    

    def test_if_non_admin_user_can_get_only_their_account(self):
        self.client.force_login(self.premium_user)

        response = self.client.get(reverse('api:account-accounts'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    

    def test_if_user_has_access_to_their_account(self):
        self.client.force_login(self.enterprise_user)
        self.account = self.accounts[2]

        response = self.client.get(reverse('api:account-single-account', kwargs={'pk': self.account.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_if_admin_has_access_to_not_their_account(self):
        self.account = self.accounts[2]
        response = self.client.get(reverse('api:account-single-account', kwargs={'pk': self.account.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_if_non_admin_user_has_no_access_to_not_their_account(self):
        self.client.force_login(self.basic_user)

        self.account = self.accounts[2]
        response = self.client.get(reverse('api:account-single-account', kwargs={'pk': self.account.id}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)