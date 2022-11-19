from django.urls import reverse
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile

from tests.test_api.test_setup import TestSetUp

class TestImageViews(TestSetUp):
    def test_basic_user_can_post_image(self):
        self.client.force_login(self.basic_user)
        self.account = self.accounts[0]

        try: 
            file = open(self.prepare_images["to_upload"], "rb")
            self.image_file = SimpleUploadedFile(
                name=file.name,
                content=file.read(),
                content_type='image/jpg'
                )
            self.image_data = {
                'image_file': self.image_file,
                'caption': 'basicuser_image',
                'account': self.account.id
            }

            response = self.client.post(reverse('api:image-images', kwargs={'pk': self.account.id}), data=self.image_data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        finally:
            file.close()
    

    def test_custom_user_can_post_image(self):
        self.client.force_login(self.custom_user)
        self.account = self.accounts[3]

        try: 
            file = open(self.prepare_images["to_upload"], "rb")
            self.image_file = SimpleUploadedFile(
                name=file.name,
                content=file.read(),
                content_type='image/jpg'
                )
            self.image_data = {
                'image_file': self.image_file,
                'caption': 'basicuser_image',
                'account': self.account.id
            }

            response = self.client.post(reverse('api:image-images', kwargs={'pk': self.account.id}), data=self.image_data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        finally:
            file.close()


    def test_premium_user_can_list_their_images(self):
        self.client.force_login(self.premium_user)
        self.account = self.accounts[1]
        response = self.client.get(reverse('api:image-images', kwargs={'pk': self.account.id}))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


    def test_custom_user_can_list_their_images(self):
        self.client.force_login(self.custom_user)
        self.account = self.accounts[3]

        response = self.client.get(reverse('api:image-images', kwargs={'pk': self.account.id}))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    
    def test_enterprise_user_can_get_correct_thumbnails(self):
        self.client.force_login(self.enterprise_user)
        self.account = self.accounts[2]
        
        response = self.client.get(reverse('api:image-single-image', kwargs={
            'pk': self.account.id, 'image_pk': self.images[2].id
            }))

        self.access_to_original = self.account.account_tier.original_link == True
        self.thumbnails_amount = len(self.account.account_tier.thumbnail_sizes.split(","))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["image_file"]), self.thumbnails_amount + self.access_to_original)

    
    def test_custom_user_can_get_correct_thumbnails(self):
        self.client.force_login(self.custom_user)
        self.account = self.accounts[3]

        response = self.client.get(reverse('api:image-single-image', kwargs={
            'pk': self.account.id, 'image_pk': self.images[3].id
            }))

        self.access_to_original = self.account.account_tier.original_link == True
        self.thumbnails_amount = len(self.account.account_tier.thumbnail_sizes.split(","))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["image_file"]), self.thumbnails_amount + self.access_to_original)


    def test_admin_can_get_images_of_other_user(self):
        self.account = self.accounts[3]
        response = self.client.get(reverse('api:image-images', kwargs={'pk': self.account.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    
    def test_non_admin_user_cannot_get_images_of_other_user(self):
        self.client.force_login(self.basic_user)
        self.account = self.accounts[1]   

        response = self.client.get(reverse('api:image-images', kwargs={'pk': self.account.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_admin_can_get_thumbnails_of_other_user(self):
        self.account = self.accounts[1]

        response = self.client.get(reverse('api:image-single-image', kwargs={
            'pk': self.account.id, 'image_pk': self.images[1].id
            }))

        self.access_to_original = self.account.account_tier.original_link == True
        self.thumbnails_amount = len(self.account.account_tier.thumbnail_sizes.split(","))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["image_file"]), self.thumbnails_amount + self.access_to_original)
    

    def test_non_admin_user_cannot_get_thumbnails_of_other_user(self):
        self.client.force_login(self.premium_user)
        self.account = self.accounts[2]

        response = self.client.get(reverse('api:image-single-image', kwargs={
            'pk': self.account.id, 'image_pk': self.images[2].id
            }))

        self.access_to_original = self.account.account_tier.original_link == True
        self.thumbnails_amount = len(self.account.account_tier.thumbnail_sizes.split(","))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)