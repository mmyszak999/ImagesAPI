from django.urls import path

from api import views

app_name = 'api'

urlpatterns = [
    path('accounts/', views.AccountView.as_view({'get': 'get_all'}),
         name='account-accounts'),
    path('accounts/<int:pk>/', views.AccountDetailView.as_view({'get': 'get_one'}),
         name='account-single-account'),
    path('accounts/<int:pk>/images/', views.ImageView.as_view({'get': 'get', 'post': 'post'}),
         name='image-images'),
    path('accounts/<int:pk>/images/<int:image_pk>/', views.ImageDetailView.as_view({'get': 'get_one'}),
         name='image-single-image')
]
"""path('accounts/<int:pk>/images/<int:image_pk>/media/', views.ImageMediaView.as_view({'get': 'get'}),
         name='image-media'),"""
