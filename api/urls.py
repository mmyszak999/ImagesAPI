from django.urls import path

from api import views

app_name = 'api'

urlpatterns = [
    path('account/', views.AccountView.as_view({'get': 'get_all'}),
         name='account-accounts'),
    path('account/<int:pk>/', views.AccountDetailView.as_view({'get': 'get_one'}),
         name='account-single-account'),
    path('account/<int:pk>/image/', views.ImageView.as_view({'get': 'get', 'post': 'post'}),
         name='image-images'),
    path('account/<int:pk>/image/<int:image_pk>/', views.ImageDetailView.as_view({'get': 'get_one'}),
         name='image-single-image'),
    path('account/<int:pk>/image/<int:image_pk>/media/', views.ImageMediaView.as_view({'get': 'get'}),
         name='image-media'),
]

