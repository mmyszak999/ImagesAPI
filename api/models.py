from django.db import models
from django.core.validators import validate_comma_separated_integer_list
from versatileimagefield.fields import VersatileImageField, PPOIField


class AccountTier(models.Model):
    tier_name = models.CharField(max_length=75, default="Basic")
    thumbnail_sizes = models.CharField(max_length=150, validators=[validate_comma_separated_integer_list],
                                       null=True, default=None)
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


class Image(models.Model):
    width = models.PositiveIntegerField(default=0)
    height = models.PositiveIntegerField(default=0)
    image_file = VersatileImageField(
        'Image',
        upload_to='images/',
        ppoi_field='image_ppoi',
        width_field='width',
        height_field='height'
    )
    caption = models.CharField(max_length=75, default=None, blank=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    image_ppoi = PPOIField()

    def __str__(self):
        return self.caption


class ExpiringLinkToken(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, default=None)
    expiration_date = models.DateTimeField()
    expires_in = models.IntegerField(default=0)

    def __str__(self):
        return self.image.caption