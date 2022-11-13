from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404


from api.serializers import (
    ImageInputSerializer, ImageOutputSerializer, AccountOutputSerializer,
)
from api.models import Image, Account, AccountTier


class AccountView(GenericViewSet, ListModelMixin):
    serializer_class = AccountOutputSerializer

    def get_queryset(self):
        qs = Account.objects.all()
        if self.request.user.is_staff or self.request.user.is_superuser:
            return qs
        return qs.filter(owner=self.request.user)

    def get_serializer_class(self):
        return AccountOutputSerializer

    def get_all(self, request: Request) -> Response:
        return self.list(request)


class AccountDetailView(GenericViewSet, RetrieveModelMixin):
    def get_object(self):
        pk = self.kwargs['pk']
        obj = Account.objects.get(pk=pk)
        if (
                self.request.user.is_staff or
                self.request.user.is_superuser or
                self.request.user == obj.owner
        ):
            return obj
        return get_object_or_404(Account.objects.filter(owner=self.request.user), pk=pk)

    def get_serializer_class(self):
        return AccountOutputSerializer

    def get_one(self, request: Request, pk: int) -> Response:
        return self.retrieve(request, pk)


class ImageView(GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = ImageInputSerializer
    model = Image

    def get_queryset(self):
        images = Image.objects.filter(account=self.kwargs["pk"]).select_related("account")
        account = Account.objects.get(pk=self.kwargs['pk'])
        user = self.request.user
        if user.is_staff or user.is_superuser or account.owner == user:
            return images
        raise NotFound

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