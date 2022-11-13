from django.db import models

from api.custom_fields import CommaSepField


class AccountTier(models.Model):
    tier_name = models.CharField(max_length=75, default="Basic")
    thumbnail_sizes = CommaSepField()
    original_link = models.BooleanField(default=False)
    expiring_links = models.BooleanField(default=False)
    min_expiring_time = models.PositiveIntegerField(default=0)
    max_expiring_time = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.tier_name


class Account(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    account_tier = models.ForeignKey(AccountTier, on_delete=models.CASCADE)

    def __str__(self):
        return self.owner.username


class Thumbnail(models.Model):
    thumbnail = models.ImageField(upload_to='images/', default=None, blank=True)


class Image(models.Model):
    image_file = models.ImageField(
        upload_to="images/", default=None, blank=True, height_field='image_height', width_field='image_width'
    )
    image_height = models.PositiveIntegerField(default=0)
    image_width = models.PositiveIntegerField(default=0)
    thumbnails = models.ForeignKey(Thumbnail, on_delete=models.CASCADE)
    caption = models.CharField(max_length=75, default=None, blank=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.caption







