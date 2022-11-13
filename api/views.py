from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response

from api.serializers import (
    ImageInputSerializer, ImageOutputSerializer, AccountOutputSerializer,
    AccountTierInputSerializer, AccountTierOutputSerializer
)
from api.models import Image, Account, AccountTier


class ImageView(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = Image.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ImageOutputSerializer
        return ImageInputSerializer

    def get(self, request: Request, pk: int) -> Response:
        return self.list(request, pk)

    def post(self, request: Request, pk: int) -> Response:
        return self.create(request, pk)


class ImageDetailView(GenericViewSet, RetrieveModelMixin):
    queryset = Image.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ImageOutputSerializer
        return ImageInputSerializer

    def get_one(self, request: Request, pk: int, image_pk: int) -> Response:
        return self.retrieve(request, pk, image_pk)


class AccountView(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = Account.objects.all()

    def get_serializer_class(self):
        return AccountOutputSerializer

    def get(self, request: Request) -> Response:
        return self.list(request)


class AccountDetailView(GenericViewSet, RetrieveModelMixin):
    queryset = Account.objects.all()

    def get_serializer_class(self):
        return AccountOutputSerializer

    def get_one(self, request: Request, pk: int) -> Response:
        return self.retrieve(request, pk)


class AccountTierView(GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = AccountTier.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AccountTierOutputSerializer
        return AccountTierInputSerializer

    def get(self, request: Request) -> Response:
        return self.list(request)

    def post(self, request: Request) -> Response:
        return self.create(request)


class AccountTierDetailView(GenericViewSet, RetrieveModelMixin):
    queryset = AccountTier.objects.all()

    def get_serializer_class(self):
        return AccountTierOutputSerializer

    def get_one(self, request: Request, pk: int) -> Response:
        return self.retrieve(request, pk)


