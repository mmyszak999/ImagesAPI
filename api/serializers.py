from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    ImageField,
    ReadOnlyField,
    IntegerField,
    CharField,
    HyperlinkedRelatedField
)
from versatileimagefield.serializers import VersatileImageFieldSerializer   

from api.models import Image, Account, ExpiringLinkToken


class AccountOutputSerializer(ModelSerializer):
    owner_name = ReadOnlyField(source='owner.username')
    tier_name = ReadOnlyField(source='account_tier.tier_name')

    class Meta:
        model = Account
        fields = ('id', 'owner', 'account_tier', 'owner_name', 'tier_name',)
        read_only_fields = fields


class ImageInputSerializer(Serializer):
    image_file = ImageField()
    caption = CharField()


class ImageOutputSerializer(ModelSerializer):
    image_name = ReadOnlyField(source="image_file.name")

    class Meta:
        model = Image
        fields = ('id', 'caption', 'account', 'width', 'height', 'image_name',)
        read_only_fields = fields


class ImageMediaSerializer(ModelSerializer):

    image_file = VersatileImageFieldSerializer(
        sizes='media_sizes')

    class Meta:
        model = Image
        fields = ('id', 'image_file',)
        read_only_fields = fields


class ExpringLinkTokenInputSerializer(Serializer):
    expires_in = IntegerField()


class ExpiringLinkTokenOutputSerializer(ModelSerializer):
    image_url = HyperlinkedRelatedField(
        view_name='api:image-get-expiring-link',
        lookup_field="image_pk",
        read_only=True
    )

    class Meta:
        model = ExpiringLinkToken
        fields = ("id", "image_url", "expires_in", "expiration_date")
        read_only_fields = fields


class ExpiringLinkImageOutputSerializer(ModelSerializer):

    class Meta:
        model = Image
        fields = ("image_file",)
        read_only_fields = fields