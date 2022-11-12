from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response

from api.serializers import (
    ImageInputSerializer, ImageOutputSerializer, AccountOutputSerializer, AccountInputSerializer
)
from api.models import Image, Account


class ImageView(GenericViewSet, ListModelMixin):
    queryset = Image.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ImageOutputSerializer
        return ImageInputSerializer

    def get(self, request: Request) -> Response:
        return self.list(request)

    def create(self, request: Request) -> Response:
        pass


class AccountView(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = Account.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AccountOutputSerializer
        return AccountInputSerializer

    def get(self, request: Request) -> Response:
        return self.list(request)


class AccountDetailView(GenericViewSet, RetrieveModelMixin):
    queryset = Account.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AccountOutputSerializer
        return AccountInputSerializer

    def get_one(self, request: Request, pk: int) -> Response:
        return self.retrieve(request, pk)

