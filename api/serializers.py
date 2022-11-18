from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    ImageField,
    ReadOnlyField,
    IntegerField,
    CharField
)
from versatileimagefield.serializers import VersatileImageFieldSerializer
from versatileimagefield.fields import VersatileImageField

from api.models import Image, Account, AccountTier, Thumbnail


class ImageInputSerializer(Serializer):
    image_file = ImageField()
    caption = CharField()


class ImageOutputSerializer(ModelSerializer):
    image_name = ReadOnlyField(source="image_file.name")

    class Meta:
        model = Image
        fields = ('id', 'caption', 'account', 'width', 'height', 'image_name')
        read_only_fields = fields


class ImageMediaSerializer(ModelSerializer):

    image_file = VersatileImageFieldSerializer(
        sizes='media_sizes')

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
