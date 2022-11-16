from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    ImageField,
    ReadOnlyField,
    IntegerField
)
from versatileimagefield.serializers import VersatileImageFieldSerializer
from versatileimagefield.fields import VersatileImageField

from api.models import Image, Account, AccountTier, Thumbnail


class ImageInputSerializer(ModelSerializer):

    class Meta:
        model = Image
        fields = ('id', 'image_file', 'caption', 'account')


class ImageOutputSerializer(ModelSerializer):
    image_name = ReadOnlyField(source="image_file.name")

    class Meta:
        model = Image
        fields = ('id', 'caption', 'account', 'width', 'height', 'image_name')
        read_only_fields = fields


class ImageMediaSerializer(ModelSerializer):

    image_file = VersatileImageFieldSerializer(
        sizes='media_sizes')
    print('serializer', image_file.sizes)

    class Meta:
        model = Image
        fields = ('id', 'image_file')


class AccountOutputSerializer(ModelSerializer):
    owner_name = ReadOnlyField(source='owner.username')
    tier_name = ReadOnlyField(source='account_tier.tier_name')

    class Meta:
        model = Account
        fields = ('id', 'owner', 'account_tier', 'owner_name', 'tier_name',)
        read_only_fields = fields



"""class AccountTierInputSerializer(Serializer):
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
        read_only_fields = fields"""
