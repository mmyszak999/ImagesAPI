from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    CharField,
    ImageField,
    BooleanField,
    ReadOnlyField,
    IntegerField

)

from api.models import Image, Account, AccountTier, Thumbnail
from api.custom_fields import CommaSepField


class ImageInputSerializer(Serializer):
    caption = CharField()
    image = ImageField()


class ImageOutputSerializer(ModelSerializer):
    image_name = ReadOnlyField(source='image.name')
    image_owner = ReadOnlyField(source='account.owner.username')

    class Meta:
        model = Image
        fields = ('id', 'caption', 'thumbnails', 'image_name', 'image_owner',)
        read_only_fields = fields


class AccountOutputSerializer(ModelSerializer):
    owner_name = ReadOnlyField(source='owner.username')
    tier_name = ReadOnlyField(source='account_tier.tier_name')

    class Meta:
        model = Account
        fields = ('id', 'owner', 'account_tier', 'owner_name', 'tier_name',)
        read_only_fields = fields


class AccountTierInputSerializer(Serializer):
    tier_name = CharField()
    thumbnail_sizes = CharField()
    original_link = BooleanField()
    expiring_links = BooleanField()
    min_expiring_time = IntegerField()
    max_expiring_time = IntegerField()


class AccountTierOutputSerializer(ModelSerializer):
    class Meta:
        model = AccountTier
        fields = ('id', 'tier_name',
                  'thumbnail_sizes', 'original_link', 'expiring_links',
                  'min_expiring_time', 'max_expiring_time',)
        read_only_fields = fields



