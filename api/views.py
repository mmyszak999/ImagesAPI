from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from api.models import Image, Account
from api.serializers import (
    ImageInputSerializer, ImageOutputSerializer, AccountOutputSerializer, ImageMediaSerializer
)
from api.services import ImageMediaCreate, ImageCreateService
from images_api_project.settings import VERSATILEIMAGEFIELD_RENDITION_KEY_SETS, DEBUG


class AccountView(ListAPIView, GenericAPIView): 
    serializer_class = AccountOutputSerializer

    def get_queryset(self):
        qs = Account.objects.all()
        if self.request.user.is_staff or self.request.user.is_superuser:
            return qs
        return qs.filter(owner=self.request.user)

    def get_serializer_class(self):
        return AccountOutputSerializer


class AccountDetailView(RetrieveAPIView, GenericAPIView):
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


class ImageView(ListAPIView, CreateAPIView, GenericAPIView):
    model = Image

    def get_queryset(self):
        images = Image.objects.filter(account=self.kwargs["pk"]).select_related("account")
        account = Account.objects.get(pk=self.kwargs['pk'])
        user = self.request.user
        if user.is_staff or user.is_superuser or account.owner == user:
            return images
        raise NotFound(code=HTTP_404_NOT_FOUND)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ImageOutputSerializer
        return ImageInputSerializer

    def create(self, request: Request, pk: int) -> Response:
        image_create_service = ImageCreateService(request, pk)
        image_instance = image_create_service.image_create()

        return Response(self.get_serializer(image_instance).data, status=HTTP_201_CREATED)


class ImageDetailView(RetrieveAPIView, GenericAPIView):
    queryset = Image.objects.all()

    def get_object(self):
        pk = self.kwargs['image_pk']
        account_id = self.kwargs['pk']
        image = Image.objects.filter(account=account_id).select_related('account')
        if self.request.user.is_superuser:
            return get_object_or_404(image, pk=pk)
        return get_object_or_404(Image, pk=pk, account__owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ImageMediaSerializer
        return ImageInputSerializer

    def get(self, request: Request, pk: int, image_pk: int) -> Response:
        service = ImageMediaCreate()
        instance = self.get_object()
        sizes = service.create_sizes_schema(pk, instance)

        if DEBUG:
            VERSATILEIMAGEFIELD_RENDITION_KEY_SETS['media_sizes'] = sizes

        return self.retrieve(request, pk, image_pk)