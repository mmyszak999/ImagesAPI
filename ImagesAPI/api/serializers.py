from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    CharField,
    ImageField,
    ChoiceField,
    ReadOnlyField
)

from api.models import Image, Account
from api.enums import ACCOUNT_TIERS



class ImageInputSerializer(Serializer):
    caption = CharField()
    image = ImageField()


class ImageOutputSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class AccountInputSerializer(Serializer):
    account_tier = ChoiceField(choices=ACCOUNT_TIERS)


class AccountOutputSerializer(ModelSerializer):
    owner_name = ReadOnlyField(source='owner.username')

    class Meta:
        model = Account
        fields = ['id', 'owner', 'account_tier', 'owner_name']

