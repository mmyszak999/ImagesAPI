from django.db import models

from api.enums import ACCOUNT_TIERS


class Account(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    account_tier = models.CharField(max_length=100, choices=ACCOUNT_TIERS, default='Basic')


class Image(models.Model):
    image_file = models.ImageField(
        upload_to="images/", default=None, blank=True, height_field='image_height'
    )
    image_height = models.PositiveIntegerField(default=0)
    thumbnail = models.ImageField(upload_to='images/', default=None, blank=True)
    caption = models.CharField(max_length=75, default=None, blank=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.caption







