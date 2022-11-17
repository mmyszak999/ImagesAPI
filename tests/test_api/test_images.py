import os

from django.urls import reverse
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile

from tests.test_api.test_setup import TestSetUp
from ImagesAPIproject.settings import BASE_DIR


class TestImages(TestSetUp):
    def test_create_image(self):
        self.client.force_login(self.basic_user)
        self.basicaccount = self.accounts[0]
        self.premiumaccount = self.accounts[1]
        self.image_file1 = open(
            os.path.join(BASE_DIR, 'tests/test_images/basicuser.PNG'), "rb"
        )
        self.image_file2 = open(
            os.path.join(BASE_DIR, 'tests/test_images/premiumuser.JPG'), "rb"
        )

        self.image_data1 = {
            'image_file': SimpleUploadedFile(
                name=self.image_file1.name,
                content=self.image_file1.read(),
                content_type='image/png'
            ),
            'caption': 'basicuser_image',
            'account': self.basicaccount.id
        }

        self.image_data2 = {
            'image_file': SimpleUploadedFile(
                name=self.image_file2.name,
                content=self.image_file2.read(),
                content_type='image/jpg'
            ),
            'caption': 'premiumuser_image',
            'account': self.premiumaccount.id
        }

        response_post1 = self.client.post(reverse('api:image-images', kwargs={'pk': self.basicaccount.id}),
                                          data=self.image_data1)
        print(response_post1.data)
        self.assertEqual(response_post1.status_code, status.HTTP_201_CREATED)

        self.client.force_login(self.premium_user)
        response_post2 = self.client.post(reverse('api:image-images', kwargs={'pk': self.premiumaccount.id}),
                                          data=self.image_data2)
        print(response_post2.data)
        self.assertEqual(response_post2.status_code, status.HTTP_201_CREATED)

        response_get2 = self.client.get(
            reverse('api:image-single-image', kwargs={'pk': self.premiumaccount.id, 'image_pk': 2}))
        print(response_get2.data)

        self.client.force_login(self.basic_user)
        response_get1 = self.client.get(
            reverse('api:image-single-image', kwargs={'pk': self.basicaccount.id, 'image_pk': 1}))
        print(response_get1.data)
