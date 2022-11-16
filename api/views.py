from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.models import Image, Account
from api.serializers import (
    ImageInputSerializer, ImageOutputSerializer, AccountOutputSerializer, ImageMediaSerializer
)
from api.services import ImageMediaCreate
from ImagesAPI.settings import VERSATILEIMAGEFIELD_RENDITION_KEY_SETS, DEBUG


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
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request: Request, pk: int) -> Response:
        return self.create(request, pk)


class ImageDetailView(GenericViewSet, RetrieveModelMixin):
    queryset = Image.objects.all()

    def get_object(self):
        pk = self.kwargs['image_pk']
        account_id = self.kwargs['pk']
        image = Image.objects.filter(account=account_id).select_related('account')
        if self.request.user.is_superuser:
            return get_object_or_404(image, pk=pk)
        return get_object_or_404(Image, pk=pk, task_list__owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ImageOutputSerializer
        return ImageInputSerializer

    def get_one(self, request: Request, pk: int, image_pk: int) -> Response:
        return self.retrieve(request, pk, image_pk)


class ImageMediaView(GenericViewSet, RetrieveModelMixin):
    serializer_class = ImageMediaSerializer
    queryset = Image.objects.all()

    def get_object(self):
        pk = self.kwargs['image_pk']
        account_id = self.kwargs['pk']
        image = Image.objects.filter(account=account_id).select_related('account')
        if self.request.user.is_superuser:
            return get_object_or_404(image, pk=pk)
        return get_object_or_404(Image, pk=pk, task_list__owner=self.request.user)

    def get(self, request: Request, pk: int, image_pk: int) -> Response:
        service = ImageMediaCreate()
        instance = self.get_object()
        account_tier = service.get_account_tier_instance(pk)
        thumbnail_sizes = service.get_thumbnail_sizes_list(account_tier)
        original_link_access = service.check_access_to_original_image(account_tier)
        sizes = service.create_sizes_schema(thumbnail_sizes, original_link_access, instance)

        if DEBUG:
            VERSATILEIMAGEFIELD_RENDITION_KEY_SETS['media_sizes'] = sizes

        return self.retrieve(request, pk, image_pk)