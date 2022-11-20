from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.status import HTTP_201_CREATED,  HTTP_200_OK

from api.models import Image, Account, ExpiringLinkToken
from api.serializers import (
    ImageInputSerializer, ImageOutputSerializer, AccountOutputSerializer,
    ImageMediaSerializer, ExpringLinkTokenInputSerializer, ExpiringLinkTokenOutputSerializer,
    ExpiringLinkImageOutputSerializer
)
from api.services import (
    ImageMediaCreateService, ImageCreateService, ExpringLinkCreateService, GetTokenImageService
)
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
        pk = self.kwargs['pk']
        account = Account.objects.get(pk=pk)
        user = self.request.user
        images = Image.objects.filter(account=account)
        
        if (
                user.is_staff or
                user.is_superuser or
                user == account.owner
        ):
            return get_list_or_404(images)
        raise NotFound

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ImageOutputSerializer
        return ImageInputSerializer

    def create(self, request: Request, pk: int) -> Response:
        image_create_service = ImageCreateService(request, pk)
        image_instance = image_create_service.image_create()

        return Response(self.get_serializer(image_instance).data, status=HTTP_201_CREATED)


class ImageDetailView(RetrieveAPIView, GenericAPIView):
    def get_object(self):
        image_id = self.kwargs['image_pk']
        account_id = self.kwargs['pk']
        account = Account.objects.get(id=account_id)
        image = Image.objects.filter(account=account).select_related('account')
        if self.request.user.is_superuser or account.owner == self.request.user:
            return get_object_or_404(image, pk=image_id)
        raise NotFound

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ImageMediaSerializer
        return ImageInputSerializer

    def get(self, request: Request, pk: int, image_pk: int) -> Response:
        service = ImageMediaCreateService()
        instance = self.get_object()
        sizes = service.create_sizes_schema(pk, instance)

        if DEBUG:
            VERSATILEIMAGEFIELD_RENDITION_KEY_SETS['media_sizes'] = sizes

        return self.retrieve(request, pk, image_pk)


class ExpiringLinkView(CreateAPIView, ListAPIView, GenericAPIView):
    model = ExpiringLinkToken

    def get_queryset(self):
        tokens = ExpiringLinkToken.objects.filter(image=self.kwargs["image_pk"]).select_related("image")
        user = self.request.user
        image = Image.objects.get(id=self.kwargs["image_pk"])
        account = image.account
        if user.is_staff or user.is_superuser or (
            user == account.owner and
            account.account_tier.expiring_links and
            account.id == self.kwargs["pk"]
            ):
            return get_list_or_404(tokens)
        raise NotFound
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ExpiringLinkTokenOutputSerializer
        return ExpringLinkTokenInputSerializer
    
    def create(self, request: Request, pk: int, image_pk: int) -> Response:
        expiring_link_create_service = ExpringLinkCreateService(request, image_pk, pk)
        token_instance = expiring_link_create_service.expiring_link_create()

        return Response(self.get_serializer(token_instance).data, status=HTTP_201_CREATED)

    
class ExpiringLinkDetailView(RetrieveAPIView, GenericAPIView):
    model = ExpiringLinkToken

    def get_object(self):
        token = ExpiringLinkToken.objects.get(id=self.kwargs["token_pk"])
        image = token.image
        account = image.account
        user = self.request.user
        if self.request.user.is_superuser or (
            account.account_tier.expiring_links and
            user.id == account.owner.id and
            account.id == self.kwargs["pk"]
        ):
            return get_object_or_404(ExpiringLinkToken, pk=self.kwargs["token_pk"])
        raise NotFound
    
    def get_serializer_class(self):
        return ExpiringLinkImageOutputSerializer
    
    def get(self, request: Request, pk: int, image_pk: int, token_pk: int) -> Response:
        self.get_object()
        get_image_token_service = GetTokenImageService(token_pk)
        image = get_image_token_service.get_token_image()

        return Response(self.get_serializer(image).data,status=HTTP_200_OK)