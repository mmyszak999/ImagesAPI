from django.urls import path

from api import views

app_name = 'api'

urlpatterns = [
     path('accounts/', views.AccountView.as_view(),
         name='account-accounts'),
     path('accounts/<int:pk>/', views.AccountDetailView.as_view(),
         name='account-single-account'),
     path('accounts/<int:pk>/images/', views.ImageView.as_view(),
         name='image-images'),
     path('accounts/<int:pk>/images/<int:image_pk>/', views.ImageDetailView.as_view(),
         name='image-single-image'),
     path('accounts/<int:pk>/images/<int:image_pk>/expiring_link/', views.ExpiringLinkView.as_view(),
         name='image-create-expiring-link'),
     path('accounts/<int:pk>/images/<int:image_pk>/expiring_link/<int:token_pk>/', views.ExpiringLinkDetailView.as_view(),
         name='image-get-expiring-link')
]

"""path('accounts/<int:pk>/images/<int:image_pk>/media/', views.ImageMediaView.as_view({'get': 'get'}),
         name='image-media'),"""
