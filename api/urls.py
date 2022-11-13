from django.urls import path

from api import views

app_name = 'api'

urlpatterns = [
    path('account/', views.AccountView.as_view({'get': 'get'}),
         name='account-accounts'),
    path('account/<int:pk>/', views.AccountDetailView.as_view({'get': 'get_one'}),
         name='account-single-account'),
    path('account/<int:pk>/image/', views.ImageView.as_view({'get': 'get', 'post': 'post'}),
         name='image-images'),
    path('account/<int:pk>/image/<int:image_pk>/', views.ImageDetailView.as_view({'get': 'get_one'}),
         name='image-single-image'),
    path('account_tiers/', views.AccountTierView.as_view({'get': 'get', 'post': 'create'}),
         name='account_tier-tiers'),
    path('account_tiers/<int:pk>/', views.AccountTierDetailView.as_view({'get': 'get_one'}),
         name='account_tier-single-tier'),
]

